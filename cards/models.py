"""
Модели приложения cards.
Card — карточка для изучения слов.
Schedule — расписание повторений по алгоритму SM-2 для каждой карточки.
"""
from django.db import models
from users.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date

class Card(models.Model):
    """
    Карточка для изучения иностранного слова.
    Привязана к пользователю, содержит слово, перевод, пример, комментарий и уровень сложности.
    """
    LEVEL_CHOICES = [
        ('beginner', 'Начальный'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards', verbose_name='Владелец')
    word = models.CharField(max_length=128, verbose_name='Слово')
    translation = models.CharField(max_length=128, verbose_name='Перевод')
    example = models.TextField(blank=True, verbose_name='Пример использования')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    level = models.CharField(max_length=16, choices=LEVEL_CHOICES, default='beginner', verbose_name='Уровень')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    def __str__(self):
        """Строковое представление: слово и перевод."""
        return f'{self.word} — {self.translation}'

class Schedule(models.Model):
    """
    Расписание повторений для карточки по алгоритму SM-2.
    Хранит дату следующего повторения, интервал, эффективность, номер повторения и результат.
    """
    card = models.OneToOneField(Card, on_delete=models.CASCADE, related_name='schedule', verbose_name='Карточка')
    next_review = models.DateField(verbose_name='Дата следующего повторения')
    interval = models.PositiveIntegerField(default=1, verbose_name='Интервал (дней)')
    repetition = models.PositiveIntegerField(default=0, verbose_name='Номер повторения')
    ef = models.FloatField(default=2.5, verbose_name='Эффективность (SM-2)')
    last_result = models.BooleanField(null=True, blank=True, verbose_name='Последний результат (успех)')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    def __str__(self):
        """Строковое представление: краткая информация о расписании."""
        return f'Schedule for {self.card.word} (next: {self.next_review})'

@receiver(post_save, sender=Card)
def create_schedule_for_card(sender, instance, created, **kwargs):
    """
    Автоматически создаёт расписание повторения (Schedule) при создании новой карточки.
    """
    if created and not hasattr(instance, 'schedule'):
        Schedule.objects.create(card=instance, next_review=date.today())
