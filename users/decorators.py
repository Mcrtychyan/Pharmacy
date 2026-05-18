from functools import wraps
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages


def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(request, 'Необходимо авторизоваться')
                return redirect('login')

            if request.user.role in allowed_roles or request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            messages.error(request, 'У вас нет доступа к этой странице')
            raise PermissionDenied

        return wrapper

    return decorator


def pharmacist_required(view_func):
    return role_required(['pharmacist', 'admin'])(view_func)


def admin_required(view_func):
    return role_required(['admin'])(view_func)