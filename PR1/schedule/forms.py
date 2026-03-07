from django import forms
from .models import Teacher

class TeacherForm(forms.Form):
    """Форма для создания преподавателя с использованием forms.Form"""
    
    first_name = forms.CharField(
        label='Имя',
        max_length=50,
        help_text='Введите имя преподавателя (обязательно)',
        widget=forms.TextInput(attrs={
            'placeholder': 'Например: Иван',
            'class': 'form-control'
        })
    )
    
    last_name = forms.CharField(
        label='Фамилия',
        max_length=50,
        help_text='Введите фамилию преподавателя (обязательно)',
        widget=forms.TextInput(attrs={
            'placeholder': 'Например: Петров',
            'class': 'form-control'
        })
    )
    
    email = forms.EmailField(
        label='Email',
        help_text='Введите email преподавателя (обязательно, должен быть уникальным)',
        widget=forms.EmailInput(attrs={
            'placeholder': 'example@school.ru',
            'class': 'form-control'
        })
    )
    
    specialization = forms.CharField(
        label='Специализация',
        max_length=200,
        help_text='Введите специализацию преподавателя (обязательно)',
        widget=forms.TextInput(attrs={
            'placeholder': 'Например: Программирование',
            'class': 'form-control'
        })
    )
    
    bio = forms.CharField(
        label='Биография',
        required=False,  # Это поле необязательное
        help_text='Краткая биография преподавателя (необязательно)',
        widget=forms.Textarea(attrs={
            'placeholder': 'Расскажите о преподавателе...',
            'rows': 4,
            'class': 'form-control'
        })
    )
    
    education = forms.CharField(
        label='Образование',
        required=False,
        help_text='Образование преподавателя (необязательно)',
        widget=forms.TextInput(attrs={
            'placeholder': 'Например: МГУ, 2010',
            'class': 'form-control'
        })
    )
    
    office_number = forms.CharField(
        label='Номер кабинета',
        required=False,
        help_text='Номер кабинета (необязательно)',
        widget=forms.TextInput(attrs={
            'placeholder': 'Например: 101',
            'class': 'form-control'
        })
    )
    
    def clean_email(self):
        """Проверка уникальности email"""
        email = self.cleaned_data.get('email')
        if Teacher.objects.filter(email=email).exists():
            raise forms.ValidationError('Преподаватель с таким email уже существует')
        return email