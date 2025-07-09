"""
Формы для работы с карточками (CardForm).
Используется для создания и редактирования карточек пользователя.
"""
from django import forms
from .models import Card

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['word', 'translation', 'example', 'comment', 'level']
        widgets = {
            'word': forms.TextInput(attrs={
                'class': 'px-3 py-2 border border-gray-300 rounded-lg shadow-sm bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-200 w-full',
                'placeholder': 'Слово',
            }),
            'translation': forms.TextInput(attrs={
                'class': 'px-3 py-2 border border-gray-300 rounded-lg shadow-sm bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-200 w-full',
                'placeholder': 'Перевод',
            }),
            'example': forms.Textarea(attrs={
                'class': 'px-3 py-2 border border-gray-300 rounded-lg shadow-sm bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-200 w-full',
                'rows': 2,
                'placeholder': 'Пример использования',
            }),
            'comment': forms.Textarea(attrs={
                'class': 'px-3 py-2 border border-gray-300 rounded-lg shadow-sm bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-200 w-full',
                'rows': 2,
                'placeholder': 'Комментарий',
            }),
            'level': forms.Select(attrs={
                'class': 'px-3 py-2 border border-gray-300 rounded-lg shadow-sm bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-200 w-full',
            }),
        }

class CardImportForm(forms.Form):
    """
    Форма для загрузки CSV-файла с карточками.
    """
    file = forms.FileField(label='CSV-файл', help_text='Формат: word, translation, example, comment, level (UTF-8)') 