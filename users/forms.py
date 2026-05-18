from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
import re
from .models import CustomUser


class RegisterForm(UserCreationForm):
    full_name = forms.CharField(label='ФИО', max_length=150)
    phone = forms.CharField(label='Телефон', max_length=15)
    email = forms.EmailField(label='Email')

    class Meta:
        model = CustomUser
        fields = ('username', 'full_name', 'phone', 'email', 'password1', 'password2')
        labels = {
            'username': 'Логин'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })

        self.fields['username'].widget.attrs.update({
            'placeholder': 'Введите логин'
        })

        self.fields['full_name'].widget.attrs.update({
            'placeholder': 'Иванов Иван Иванович'
        })

        self.fields['phone'].widget.attrs.update({
            'placeholder': '8(999)123-45-67'
        })

        self.fields['email'].widget.attrs.update({
            'placeholder': 'example@mail.ru'
        })

        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Повтор пароля'

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if not re.fullmatch(r'[A-Za-z0-9]+', username):
            raise ValidationError('Логин должен содержать только латинские буквы и цифры')

        if len(username) < 6:
            raise ValidationError('Логин должен быть не короче 6 символов')

        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким логином уже существует')

        return username

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')

        if not re.fullmatch(r'[А-Яа-яЁё\s]+', full_name):
            raise ValidationError('ФИО должно содержать только кириллицу и пробелы')

        return full_name

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if not re.fullmatch(r'8\(\d{3}\)\d{3}-\d{2}-\d{2}', phone):
            raise ValidationError('Телефон должен быть в формате 8(XXX)XXX-XX-XX')

        if CustomUser.objects.filter(phone=phone).exists():
            raise ValidationError('Пользователь с таким телефоном уже существует')

        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с такой электронной почтой уже существует')

        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.full_name = self.cleaned_data.get('full_name')
        user.email = self.cleaned_data.get('email')
        user.phone = self.cleaned_data.get('phone')
        # По умолчанию при регистрации даем роль 'user'
        user.role = 'user'

        if commit:
            user.save()

        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', max_length=150)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': 'Неверный логин или пароль',
        'inactive': 'Учётная запись отключена'
    }

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })


class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'full_name', 'phone', 'role', 'is_active')
        labels = {
            'username': 'Логин',
            'email': 'Email',
            'full_name': 'ФИО',
            'phone': 'Телефон',
            'role': 'Роль',
            'is_active': 'Активен',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})