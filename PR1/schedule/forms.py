from django import forms
from django.core.exceptions import ValidationError
from .models import Teacher, TeacherInfo, Course, Student
import re
from datetime import date

# ==================== КАСТОМНЫЕ ВАЛИДАТОРЫ ====================

def validate_phone_number(value):
    """Валидатор для номера телефона"""
    if value:
        pattern = r'^\+7 \d{3} \d{3}-\d{2}-\d{2}$'
        if not re.match(pattern, value):
            raise ValidationError('Телефон должен быть в формате: +7 123 456-78-90')


def validate_experience_years(value):
    """Валидатор для стажа"""
    if value is not None:
        if value < 0:
            raise ValidationError('Стаж не может быть отрицательным')
        if value > 50:
            raise ValidationError('Стаж не может превышать 50 лет')


def validate_russian_name(value):
    """Валидатор для имени/фамилии"""
    if value and not re.match(r'^[А-Яа-яЁё]+$', value):
        raise ValidationError('Имя/Фамилия должны содержать только русские буквы')


# ==================== ФОРМА TEACHER ====================
class TeacherModelForm(forms.ModelForm):
    """Форма для преподавателя на основе модели"""
    
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'email', 'phone', 'specialization',
                  'experience_years', 'hire_date', 'is_active', 'degree', 'rating', 'salary']
        widgets = {
            'hire_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иван'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Петров'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ivan@school.ru'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 123 456-78-90'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Программирование'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '5'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '4.5', 'step': '0.01'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '50000'}),
        }
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
            'phone': 'Телефон',
            'specialization': 'Специализация',
            'experience_years': 'Стаж (лет)',
            'hire_date': 'Дата найма',
            'is_active': 'Активен',
            'degree': 'Ученая степень',
            'rating': 'Рейтинг (0-5)',
            'salary': 'Зарплата (руб)',
        }
        help_texts = {
            'first_name': 'Только русские буквы, минимум 2 символа',
            'last_name': 'Только русские буквы, минимум 2 символа',
            'phone': 'Формат: +7 123 456-78-90',
            'experience_years': 'От 0 до 50 лет',
            'rating': 'Оценка от 0 до 5',
        }
    
    # ==================== clean_методы для полей ====================
    
    def clean_first_name(self):
        """Проверка имени - ТОЛЬКО РУССКИЕ БУКВЫ"""
        first_name = self.cleaned_data.get('first_name')
        print(f"DEBUG: clean_first_name called with: {first_name}")  # для отладки
        
        if first_name:
            # Проверка на русские буквы
            if not re.match(r'^[А-Яа-яЁё]+$', first_name):
                raise ValidationError('Имя должно содержать только русские буквы')
            # Проверка на минимальную длину
            if len(first_name) < 2:
                raise ValidationError('Имя должно содержать минимум 2 буквы')
        return first_name
    
    def clean_last_name(self):
        """Проверка фамилии - ТОЛЬКО РУССКИЕ БУКВЫ"""
        last_name = self.cleaned_data.get('last_name')
        print(f"DEBUG: clean_last_name called with: {last_name}")  # для отладки
        
        if last_name:
            # Проверка на русские буквы
            if not re.match(r'^[А-Яа-яЁё]+$', last_name):
                raise ValidationError('Фамилия должна содержать только русские буквы')
            # Проверка на минимальную длину
            if len(last_name) < 2:
                raise ValidationError('Фамилия должна содержать минимум 2 буквы')
        return last_name
    
    def clean_phone(self):
        """Проверка телефона"""
        phone = self.cleaned_data.get('phone')
        if phone:
            pattern = r'^\+7 \d{3} \d{3}-\d{2}-\d{2}$'
            if not re.match(pattern, phone):
                raise ValidationError('Телефон должен быть в формате: +7 123 456-78-90')
        return phone
    
    def clean_experience_years(self):
        """Проверка стажа"""
        experience = self.cleaned_data.get('experience_years')
        if experience is not None:
            if experience < 0:
                raise ValidationError('Стаж не может быть отрицательным')
            if experience > 50:
                raise ValidationError('Стаж не может превышать 50 лет')
        return experience
    
    def clean_rating(self):
        """Проверка рейтинга"""
        rating = self.cleaned_data.get('rating')
        if rating is not None:
            if rating < 0 or rating > 5:
                raise ValidationError('Рейтинг должен быть от 0 до 5')
        return rating
    
    # ==================== clean() метод для формы ====================
    
    def clean(self):
        """Общая валидация формы"""
        cleaned_data = super().clean()
        experience = cleaned_data.get('experience_years')
        rating = cleaned_data.get('rating')
        
        print(f"DEBUG: clean() called - experience: {experience}, rating: {rating}")
        
        # Валидация 1: стаж и рейтинг
        if experience is not None and rating is not None:
            if experience < 5 and rating > 4.5:
                self.add_error('rating', 'Преподаватель со стажем менее 5 лет не может иметь рейтинг выше 4.5')
        
        # Валидация 2: email содержит домен
        email = cleaned_data.get('email')
        if email and '@' not in email:
            self.add_error('email', 'Email должен содержать символ @')
        
        return cleaned_data


# ==================== ФОРМА TEACHERINFO ====================
class TeacherInfoModelForm(forms.ModelForm):
    class Meta:
        model = TeacherInfo
        fields = ['bio', 'education', 'office_number', 'awards', 'languages', 'projects_count']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Расскажите о преподавателе...'}),
            'education': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'МГУ, 2010'}),
            'office_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '101'}),
            'awards': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Награды через запятую...'}),
            'languages': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Английский (C1), Французский (B2)'}),
            'projects_count': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '5'}),
        }
    
    def clean_languages(self):
        languages = self.cleaned_data.get('languages')
        if languages and len(languages) > 200:
            raise ValidationError('Список языков не должен превышать 200 символов')
        return languages


# ==================== ФОРМА COURSE ====================
class CourseModelForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'teacher', 'price', 'level', 'duration_hours', 'max_students', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название курса'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '15000'}),
            'duration_hours': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '40'}),
            'max_students': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '30'}),
        }
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title and len(title) < 3:
            raise ValidationError('Название курса должно содержать минимум 3 символа')
        return title
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise ValidationError('Цена не может быть отрицательной')
        if price is not None and price > 100000:
            raise ValidationError('Цена не может превышать 100 000 рублей')
        return price
    
    def clean(self):
        cleaned_data = super().clean()
        duration = cleaned_data.get('duration_hours')
        max_students = cleaned_data.get('max_students')
        
        if duration is not None and max_students is not None:
            if duration < 10 and max_students > 50:
                self.add_error('max_students', 'При длительности менее 10 часов максимальное количество студентов не может превышать 50')
        
        return cleaned_data


# ==================== ФОРМА STUDENT ====================
class StudentModelForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'phone', 'birth_date', 'is_active']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иван'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Петров'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ivan@mail.ru'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 123 456-78-90'}),
        }
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name:
            if not re.match(r'^[А-Яа-яЁё]+$', first_name):
                raise ValidationError('Имя должно содержать только русские буквы')
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name:
            if not re.match(r'^[А-Яа-яЁё]+$', last_name):
                raise ValidationError('Фамилия должна содержать только русские буквы')
        return last_name
    
    def clean(self):
        cleaned_data = super().clean()
        birth_date = cleaned_data.get('birth_date')
        
        if birth_date:
            if birth_date > date.today():
                self.add_error('birth_date', 'Дата рождения не может быть в будущем')
        
        return cleaned_data