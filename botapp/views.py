from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import pyttsx3, wikipedia, pyjokes, datetime, os
from .forms import UserRegisterForm
from django.http import JsonResponse
from gtts import gTTS
from .bot_core import process_voice_input
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def voice_input(request):
    if request.method == "POST":
        data = json.loads(request.body)
        text = data.get("text", "")
        result = process_voice_input(text)
        return JsonResponse(result)
    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def speak_view(request):
    response = None
    audio_url = None

    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        result = process_voice_input(user_input)
        response = result.get('response')
        audio_url = result.get('audio_url')

    return render(request, 'speak.html', {
        'response': response,
        'audio_url': audio_url
    })


def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.userprofile.phone_number = form.cleaned_data.get('phone_number')
            user.userprofile.address = form.cleaned_data.get('address')
            user.userprofile.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

def features(request):
    return render(request, 'features.html')

