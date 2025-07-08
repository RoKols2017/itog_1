from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views import View
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import User
import secrets
from django.urls import reverse
from django.http import HttpResponseRedirect
import base64
try:
    import qrcode
    from io import BytesIO
except ImportError:
    qrcode = None

# Create your views here.

class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
        return render(request, 'users/register.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = CustomAuthenticationForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
        return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    return render(request, 'users/profile.html', {'user': request.user})

def generate_telegram_link(request):
    if request.method == 'POST':
        user = request.user
        # Генерируем уникальный токен
        token = secrets.token_urlsafe(32)
        user.telegram_link_token = token
        user.save()
        # Формируем magic-ссылку
        telegram_link = f'https://t.me/YOUR_BOT_USERNAME?start={token}'
        telegram_qr = None
        if qrcode:
            qr = qrcode.make(telegram_link)
            buffer = BytesIO()
            qr.save(buffer, format='PNG')
            telegram_qr = base64.b64encode(buffer.getvalue()).decode('utf-8')
        # Передаём ссылку и QR в профиль
        return render(request, 'users/profile.html', {
            'user': user,
            'telegram_link': telegram_link,
            'telegram_qr': telegram_qr,
        })
    return HttpResponseRedirect(reverse('profile'))
