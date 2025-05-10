import os
import uuid
import socket
import datetime
import webbrowser
import pyjokes
import wikipedia
import pywhatkit
import requests
import random
from bs4 import BeautifulSoup
from gtts import gTTS
import playsound
import speech_recognition as sr
from GoogleNews import GoogleNews
from countryinfo import CountryInfo
from deep_translator import GoogleTranslator
from django.conf import settings

def internet_connected():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except:
        return False

def say(text):
    if not os.path.exists(settings.MEDIA_ROOT):
        os.makedirs(settings.MEDIA_ROOT)
    filename = f"say_{uuid.uuid4().hex}.mp3"
    filepath = os.path.join(settings.MEDIA_ROOT, filename)
    try:
        tts = gTTS(text=text, lang='en')
        tts.save(filepath)
        playsound.playsound(filepath)
    except Exception as e:
        print(f"[say()] 🔴 Error generating audio: {e}")

def wish_me():
    hour = datetime.datetime.now().hour
    greeting = "Good Morning" if hour < 12 else "Good Afternoon" if hour < 18 else "Good Evening"
    say(f"{greeting}! I am Chintu. How may I assist you?")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
    except:
        return "None"
    return query.lower()

def calculate(query):
    try:
        expression = query.replace("calculate", "").strip()
        result = eval(expression)
        return f"The result is {result}"
    except:
        return "Sorry, I couldn't perform the calculation."

def get_quote():
    quotes = [
        "Believe in yourself and all that you are.",
        "Success is not final, failure is not fatal: It is the courage to continue that counts.",
        "Your limitation—it’s only your imagination.",
        "Push yourself, because no one else is going to do it for you."
    ]
    return random.choice(quotes)

def process_voice_input(text):
    response = "Sorry, I didn't get that."

    try:
        if "hello" in text or "hi" in text:
            response = "Hello! How can I help you?"

        elif "joke" in text:
            response = pyjokes.get_joke()

        elif "time" in text:
            response = datetime.datetime.now().strftime("%H:%M:%S")

        elif "weather in" in text:
            city = text.split("in")[-1].strip()
            url = f"https://www.google.com/search?q=weather+in+{city}"
            soup = BeautifulSoup(requests.get(url).text, "html.parser")
            temp = soup.find("div", class_="BNeawe").text
            response = f"Current weather in {city} is {temp}"

        elif "wikipedia" in text:
            query = text.replace("wikipedia", "").strip()
            response = wikipedia.summary(query, sentences=2)

        elif "capital of" in text:
            country = text.replace("capital of", "").strip()
            capital = CountryInfo(country).capital()
            response = f"The capital of {country} is {capital}"

        elif "play" in text:
            song = text.replace("play", "").strip()
            response = f"Playing {song} on YouTube"
            pywhatkit.playonyt(song)

        elif "news" in text:
            news = GoogleNews(lang='en')
            news.search('India')
            news.getpage(1)
            headlines = news.gettext()
            response = "Top headlines are: " + ', '.join(headlines[:3])

        elif "translate" in text:
            message = text.replace("translate", "").strip()
            result = GoogleTranslator(source='auto', target='hi').translate(message)
            response = result

        elif "calculate" in text:
            response = calculate(text)

        elif "quote" in text:
            response = get_quote()

    except Exception as e:
        print("🔴 Error:", e)
        response = "Oops! Something went wrong."

    filename = f"tts_{uuid.uuid4().hex}.mp3"
    filepath = os.path.join(settings.MEDIA_ROOT, filename)

    try:
        tts = gTTS(text=response, lang='en')
        tts.save(filepath)
    except Exception as e:
        print("🔴 TTS error:", e)

    return {
        "response": response,
        "audio_url": f"{settings.MEDIA_URL}{filename}"
    }
