"""
Модуль для обращения к Yandex SpeechKit (TTS), кеширования аудиофайлов и очистки кеша по TTL.
"""
import os
import requests
import hashlib
import time
from pathlib import Path
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
YANDEX_API_KEY = os.getenv('YANDEX_SPEECHKIT_API_KEY')
YANDEX_FOLDER_ID = os.getenv('YANDEX_SPEECHKIT_FOLDER_ID')
AUDIO_CACHE_TTL = int(os.getenv('AUDIO_CACHE_TTL', 604800))  # 7 дней по умолчанию
AUDIO_CACHE_DIR = Path('media/audio')
AUDIO_CACHE_DIR.mkdir(parents=True, exist_ok=True)

SPEECHKIT_URL = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'


def get_audio_cache_path(text, lang='en-US', voice='alena'):
    """
    Возвращает путь к аудиофайлу для данного текста и параметров.
    """
    key = f'{text}|{lang}|{voice}'
    h = hashlib.sha256(key.encode('utf-8')).hexdigest()
    return AUDIO_CACHE_DIR / f'{h}.ogg'


def synthesize_speech(text, lang='en-US', voice='alena'):
    """
    Получает аудиофайл для текста через Yandex SpeechKit с кешированием.
    Возвращает путь к аудиофайлу (ogg).
    """
    audio_path = get_audio_cache_path(text, lang, voice)
    # Проверка кеша
    if audio_path.exists():
        mtime = audio_path.stat().st_mtime
        if time.time() - mtime < AUDIO_CACHE_TTL:
            return str(audio_path)
    # Запрос к Yandex SpeechKit
    headers = {
        'Authorization': f'Api-Key {YANDEX_API_KEY}',
    }
    data = {
        'text': text,
        'lang': lang,
        'voice': voice,
        'folderId': YANDEX_FOLDER_ID,
        'format': 'oggopus',
        'sampleRateHertz': '48000',
    }
    resp = requests.post(SPEECHKIT_URL, headers=headers, data=data)
    if resp.status_code == 200:
        with open(audio_path, 'wb') as f:
            f.write(resp.content)
        return str(audio_path)
    else:
        raise Exception(f'Yandex SpeechKit error: {resp.status_code} {resp.text}')


def clean_audio_cache():
    """
    Удаляет аудиофайлы старше TTL из кеша.
    """
    now = time.time()
    for file in AUDIO_CACHE_DIR.glob('*.ogg'):
        if now - file.stat().st_mtime > AUDIO_CACHE_TTL:
            try:
                file.unlink()
            except Exception:
                pass 