from django.urls import path
from . import views

urlpatterns = [
    path('telegram/bind/', views.telegram_bind, name='api_telegram_bind'),
    path('cards/', views.cards_list, name='api_cards_list'),
    path('today/', views.cards_today, name='api_cards_today'),
    path('progress/', views.user_progress, name='api_user_progress'),
    path('tts/', views.tts, name='api_tts'),
    path('test/', views.test, name='api_test'),  # опционально
] 