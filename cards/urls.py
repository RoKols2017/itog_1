"""
URL-маршруты для приложения cards.
CRUD для карточек пользователя.
"""
from django.urls import path
from .views import CardListView, CardCreateView, CardUpdateView, CardDeleteView
from .views import review_card, import_cards

urlpatterns = [
    path('', CardListView.as_view(), name='card_list'),  # Список и фильтрация карточек
    path('add/', CardCreateView.as_view(), name='card_add'),  # Создание карточки
    path('review/', review_card, name='card_review'),  # Режим повторения
    path('import/', import_cards, name='card_import'),  # Импорт карточек
    path('<int:pk>/edit/', CardUpdateView.as_view(), name='card_edit'),  # Редактирование карточки
    path('<int:pk>/delete/', CardDeleteView.as_view(), name='card_delete'),  # Удаление карточки
] 