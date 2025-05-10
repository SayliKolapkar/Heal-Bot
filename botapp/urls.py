from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('speak/', views.speak_view, name='speak'),
    path('voice-input/', views.voice_input, name='voice_input'),
    path('profile/', views.profile, name='profile'),
    path('features/', views.features, name='features'),
]