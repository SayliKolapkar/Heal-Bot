
from django.contrib import admin
from django.urls import path, include
from botapp import views as bot_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('botapp.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', bot_views.register, name='register'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)