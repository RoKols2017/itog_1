"""
Модуль SM-2 для интервального повторения карточек.
Содержит функцию update_schedule для обновления расписания по алгоритму SM-2.
"""
from datetime import date, timedelta

def update_schedule(schedule, quality):
    """
    Обновляет расписание повторения карточки по алгоритму SM-2.
    schedule: объект Schedule
    quality: int (0-5) — оценка ответа пользователя (0 — не знал, 5 — идеально)
    Меняет поля interval, repetition, ef, next_review, last_result и сохраняет расписание.
    """
    assert 0 <= quality <= 5, 'Оценка должна быть от 0 до 5'
    if quality < 3:
        schedule.repetition = 0
        schedule.interval = 1
    else:
        if schedule.repetition == 0:
            schedule.interval = 1
        elif schedule.repetition == 1:
            schedule.interval = 6
        else:
            schedule.interval = int(schedule.interval * schedule.ef)
        schedule.repetition += 1
    # Обновление эффективности (EF)
    ef = schedule.ef + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    schedule.ef = max(1.3, ef)
    # Следующая дата повторения
    schedule.next_review = date.today() + timedelta(days=schedule.interval)
    schedule.last_result = quality >= 3
    schedule.save() 