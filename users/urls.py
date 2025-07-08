from django.urls import path
from .views import RegisterView, LoginView, logout_view, profile_view, generate_telegram_link

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('generate-telegram-link/', generate_telegram_link, name='generate_telegram_link'),
] 