from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Форма для регистрации нового пользователя
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Телефон'})
    )
    birth_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'ГГГГ-ММ-ДД', 'type': 'date'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтверждение пароля'})
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'birth_date', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data.get('phone', '')
        user.birth_date = self.cleaned_data.get('birth_date')
        if commit:
            user.save()
        return user


import logging
from django import forms
from django.contrib.auth.forms import UserCreationForm
from PIL import Image
import os
from .models import CustomUser

# Создаем логгер для форм
logger = logging.getLogger(__name__)


class UserProfileForm(forms.ModelForm):
    """
    Форма для редактирования профиля пользователя
    """
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'birth_date', 'avatar', 'bio', 'city')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        
        # Получаем пользователя (если есть)
        username = self.instance.username if self.instance and self.instance.username else 'unknown'
        
        if avatar:
            # Проверка размера
            if avatar.size > 5 * 1024 * 1024:
                logger.error(f"User '{username}' failed to upload avatar: file too large ({avatar.size} bytes, max 5MB)")
                raise forms.ValidationError('Размер файла не должен превышать 5MB')
            
            # Проверка расширения файла
            ext = os.path.splitext(avatar.name)[1].lower()
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
            if ext not in allowed_extensions:
                logger.error(f"User '{username}' failed to upload avatar: invalid extension '{ext}' for file '{avatar.name}'. Allowed: {allowed_extensions}")
                raise forms.ValidationError(f'Поддерживаются только форматы: {", ".join(allowed_extensions)}')
            
            # Проверка - действительно ли это изображение
            try:
                image = Image.open(avatar)
                image.verify()
                avatar.seek(0)  # Сбрасываем указатель после verify
                
                # Успешная загрузка - логируем INFO
                logger.info(f"User '{username}' successfully uploaded avatar: '{avatar.name}' ({avatar.size} bytes)")
                
            except Exception as e:
                # ВАЖНО: Здесь логируем ERROR с exc_info=True
                logger.error(
                    f"User '{username}' tried to upload invalid image file: '{avatar.name}' - Not an image or corrupted. Error: {str(e)}",
                    exc_info=True  # Полная трассировка
                )
                raise forms.ValidationError(f'Файл не является изображением или поврежден. Ошибка: {str(e)}')
        
        return avatar