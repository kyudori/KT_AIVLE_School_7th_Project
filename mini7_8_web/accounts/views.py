from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # 비밀번호 설정
            user.save()
            user_id = form.cleaned_data.get('user_id')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(user_id=user_id, password=raw_password)
            if user is not None:
                auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('accounts:home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('accounts:home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('accounts:home')