"""
Views приложения cards: CRUD для карточек пользователя.
Только для авторизованных пользователей, только свои карточки.
Фильтрация по уровню сложности.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Card, Schedule
from .forms import CardForm, CardImportForm
import csv
from io import TextIOWrapper
from django.contrib import messages
from .sm2 import update_schedule
from datetime import date
from django.http import HttpResponseRedirect
from django.urls import reverse

@method_decorator(login_required, name='dispatch')
class CardListView(ListView):
    """
    Список карточек пользователя с фильтрацией по уровню сложности.
    Шаблон: cards/card_list.html
    """
    model = Card
    template_name = 'cards/card_list.html'
    context_object_name = 'cards'

    def get_queryset(self):
        """Фильтрует карточки по пользователю и уровню сложности (GET-параметр level)."""
        qs = Card.objects.filter(user=self.request.user).order_by('-created_at')
        level = self.request.GET.get('level')
        if level in dict(Card.LEVEL_CHOICES):
            qs = qs.filter(level=level)
        return qs

@method_decorator(login_required, name='dispatch')
class CardCreateView(CreateView):
    """
    Создание новой карточки для пользователя.
    Шаблон: cards/card_form.html
    """
    model = Card
    form_class = CardForm
    template_name = 'cards/card_form.html'
    success_url = reverse_lazy('card_list')

    def form_valid(self, form):
        """Привязывает карточку к текущему пользователю."""
        form.instance.user = self.request.user
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class CardUpdateView(UpdateView):
    """
    Редактирование карточки пользователя.
    Шаблон: cards/card_form.html
    """
    model = Card
    form_class = CardForm
    template_name = 'cards/card_form.html'
    success_url = reverse_lazy('card_list')

    def get_queryset(self):
        """Ограничивает редактирование только своими карточками."""
        return Card.objects.filter(user=self.request.user)

@method_decorator(login_required, name='dispatch')
class CardDeleteView(DeleteView):
    """
    Удаление карточки пользователя.
    Шаблон: cards/card_confirm_delete.html
    """
    model = Card
    template_name = 'cards/card_confirm_delete.html'
    success_url = reverse_lazy('card_list')

    def get_queryset(self):
        """Ограничивает удаление только своими карточками."""
        return Card.objects.filter(user=self.request.user)

@login_required
def review_card(request):
    """
    Режим повторения: показывает карточку на сегодня, принимает оценку, обновляет расписание через SM-2.
    """
    # Находим карточку пользователя, которую нужно повторить сегодня или раньше
    schedule = Schedule.objects.filter(card__user=request.user, next_review__lte=date.today()).order_by('next_review').select_related('card').first()
    if not schedule:
        return render(request, 'cards/review_done.html')
    card = schedule.card
    if request.method == 'POST':
        try:
            quality = int(request.POST.get('quality'))
            assert 0 <= quality <= 5
        except (TypeError, ValueError, AssertionError):
            messages.error(request, 'Оценка должна быть от 0 до 5')
            return HttpResponseRedirect(reverse('card_review'))
        update_schedule(schedule, quality)
        return HttpResponseRedirect(reverse('card_review'))
    return render(request, 'cards/review.html', {'card': card, 'schedule': schedule})

@login_required
def import_cards(request):
    """
    Импорт карточек из CSV-файла для текущего пользователя.
    """
    if request.method == 'POST':
        form = CardImportForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            try:
                decoded = TextIOWrapper(file, encoding='utf-8')
                reader = csv.DictReader(decoded)
                count, errors = 0, []
                for i, row in enumerate(reader, 1):
                    word = row.get('word', '').strip()
                    translation = row.get('translation', '').strip()
                    if not word or not translation:
                        errors.append(f'Строка {i}: word и translation обязательны')
                        continue
                    level = row.get('level', 'beginner').strip() or 'beginner'
                    if level not in dict(Card.LEVEL_CHOICES):
                        errors.append(f'Строка {i}: некорректный level')
                        continue
                    Card.objects.create(
                        user=request.user,
                        word=word,
                        translation=translation,
                        example=row.get('example', '').strip(),
                        comment=row.get('comment', '').strip(),
                        level=level,
                    )
                    count += 1
                if count:
                    messages.success(request, f'Импортировано карточек: {count}')
                if errors:
                    messages.error(request, 'Ошибки импорта:\n' + '\n'.join(errors))
                return HttpResponseRedirect(reverse('card_list'))
            except Exception as e:
                messages.error(request, f'Ошибка чтения файла: {e}')
    else:
        form = CardImportForm()
    return render(request, 'cards/import.html', {'form': form})
