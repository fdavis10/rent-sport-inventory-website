from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import RegisterForm, LoginForm, UserProfileForm
from .models import User


def register_view(request):
    if request.user.is_authenticated:
        return redirect('core:index')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.get_full_name()}! Регистрация прошла успешно.')
            return redirect('core:index')
    else:
        form = RegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:index')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.get_full_name() or user.username}!')
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                
                if user.role in ['MANAGER', 'ADMIN']:
                    return redirect('custom_admin:dashboard')
                else:
                    return redirect('core:index')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы.')
    return redirect('core:index')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлён!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    from rentals.models import Rental
    user_rentals = Rental.objects.filter(user=request.user)
    
    context = {
        'form': form,
        'total_rentals': user_rentals.count(),
        'active_rentals': user_rentals.filter(status=Rental.Status.ACTIVE).count(),
        'completed_rentals': user_rentals.filter(status=Rental.Status.COMPLETED).count(),
    }
    
    return render(request, 'accounts/profile.html', context)