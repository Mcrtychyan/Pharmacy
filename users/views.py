from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, UserEditForm
from .decorators import admin_required
from .models import CustomUser
from django.contrib.auth import login


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})


@admin_required
def user_list(request):
    users = CustomUser.objects.all().order_by('-date_joined')

    context = {
        'users': users,
    }
    return render(request, 'users/user_list.html', context)


@admin_required
def user_edit(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Данные пользователя {user.username} обновлены')
            return redirect('users:user_list')
    else:
        form = UserEditForm(instance=user)

    return render(request, 'users/user_edit.html', {'form': form, 'edit_user': user})


@admin_required
def user_delete(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        if user == request.user:
            messages.error(request, 'Нельзя удалить самого себя')
            return redirect('users:user_list')

        username = user.username
        user.delete()
        messages.success(request, f'Пользователь {username} удален')
        return redirect('users:user_list')

    return render(request, 'users/user_delete.html', {'delete_user': user})