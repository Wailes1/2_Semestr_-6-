from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    Форма для регистрации нового пользователя с дополнительными полями
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