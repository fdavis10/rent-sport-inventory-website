from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from functools import wraps


def admin_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.role != 'ADMIN':
            messages.error(request, 'У вас нет прав для доступа к этой странице.')
            return redirect('core:index')
        return view_func(request, *args, **kwargs)
    return wrapper


def staff_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.role not in ['ADMIN', 'MANAGER']:
            messages.error(request, 'У вас нет прав для доступа к этой странице.')
            return redirect('core:index')
        return view_func(request, *args, **kwargs)
    return wrapper