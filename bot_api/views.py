from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from users.models import User
from cards.models import Card, Schedule
from cards.speechkit import synthesize_speech
from datetime import date
import json
from django.db import models

# Create your views here.

@csrf_exempt
def telegram_bind(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    try:
        data = json.loads(request.body.decode('utf-8'))
        token = data.get('token')
        telegram_id = data.get('telegram_id')
        if not token or not telegram_id:
            return JsonResponse({'error': 'token and telegram_id required'}, status=400)
        user = User.objects.filter(telegram_link_token=token).first()
        if not user:
            return JsonResponse({'error': 'invalid token'}, status=404)
        user.telegram_id = telegram_id
        user.telegram_link_token = None
        user.save()
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_user_by_telegram_id(request):
    telegram_id = request.GET.get('telegram_id') or request.POST.get('telegram_id')
    if not telegram_id:
        return None, JsonResponse({'error': 'telegram_id required'}, status=400)
    user = User.objects.filter(telegram_id=telegram_id).first()
    if not user:
        return None, JsonResponse({'error': 'user not found'}, status=404)
    return user, None

def cards_list(request):
    user, error = get_user_by_telegram_id(request)
    if error:
        return error
    cards = Card.objects.filter(user=user)
    data = [
        {
            'id': c.id,
            'word': c.word,
            'translation': c.translation,
            'example': c.example,
            'comment': c.comment,
            'level': c.level,
        } for c in cards
    ]
    return JsonResponse({'cards': data})

def cards_today(request):
    user, error = get_user_by_telegram_id(request)
    if error:
        return error
    today = date.today()
    schedules = Schedule.objects.filter(card__user=user, next_review__lte=today).select_related('card')
    data = [
        {
            'id': s.card.id,
            'word': s.card.word,
            'translation': s.card.translation,
            'example': s.card.example,
            'comment': s.card.comment,
            'level': s.card.level,
            'next_review': s.next_review,
            'interval': s.interval,
            'repetition': s.repetition,
        } for s in schedules
    ]
    return JsonResponse({'cards': data})

def user_progress(request):
    user, error = get_user_by_telegram_id(request)
    if error:
        return error
    total = Card.objects.filter(user=user).count()
    learned = Schedule.objects.filter(card__user=user, interval__gte=21).count()  # условно "выучено"
    errors = Schedule.objects.filter(card__user=user, last_result=False).count()
    repetitions = Schedule.objects.filter(card__user=user).aggregate(total_reps=models.Sum('repetition'))['total_reps'] or 0
    return JsonResponse({
        'total': total,
        'learned': learned,
        'errors': errors,
        'repetitions': repetitions,
    })

def tts(request):
    telegram_id = request.GET.get('telegram_id')
    word = request.GET.get('word')
    if not telegram_id or not word:
        return JsonResponse({'error': 'telegram_id and word required'}, status=400)
    user = User.objects.filter(telegram_id=telegram_id).first()
    if not user:
        return JsonResponse({'error': 'user not found'}, status=404)
    card = Card.objects.filter(user=user, word=word).first()
    if not card:
        return JsonResponse({'error': 'word not found for user'}, status=404)
    try:
        audio_path = synthesize_speech(word)
        with open(audio_path, 'rb') as f:
            return HttpResponse(f.read(), content_type='audio/ogg')
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def test(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    try:
        data = json.loads(request.body.decode('utf-8'))
        telegram_id = data.get('telegram_id')
        card_id = data.get('card_id')
        answer = data.get('answer')
        if not telegram_id or not card_id or answer is None:
            return JsonResponse({'error': 'telegram_id, card_id, answer required'}, status=400)
        user = User.objects.filter(telegram_id=telegram_id).first()
        if not user:
            return JsonResponse({'error': 'user not found'}, status=404)
        card = Card.objects.filter(user=user, id=card_id).first()
        if not card:
            return JsonResponse({'error': 'card not found'}, status=404)
        # Здесь должна быть логика проверки ответа, обновления статистики и т.д.
        # Пока просто заглушка:
        return JsonResponse({'result': 'ok', 'correct': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
