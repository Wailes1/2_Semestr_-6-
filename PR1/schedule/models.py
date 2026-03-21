from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.core.exceptions import ValidationError
import re

# ==================== КАСТОМНЫЕ ВАЛИДАТОРЫ ====================

def validate_phone_number(value):
    """Валидатор для номера телефона (формат +7 XXX XXX-XX-XX)"""
    pattern = r'^\+7 \d{3} \d{3}-\d{2}-\d{2}$'
    if value and not re.match(pattern, value):
        raise ValidationError('Телефон должен быть в формате: +7 123 456-78-90')


def validate_experience_years(value):
    """Валидатор для стажа (от 0 до 50 лет)"""
    if value < 0:
        raise ValidationError('Стаж не может быть отрицательным')
    if value > 50:
        raise ValidationError('Стаж не может превышать 50 лет')


def validate_russian_name(value):
    """Валидатор для имени и фамилии (только русские буквы)"""
    if value and not re.match(r'^[А-Яа-яЁё]+$', value):
        raise ValidationError('Имя/Фамилия должны содержать только русские буквы')


# ==================== МОДЕЛЬ TEACHER ====================
class Teacher(models.Model):
    """Преподаватель"""
    first_name = models.CharField(
        max_length=50,
        verbose_name="Имя",
        validators=[validate_russian_name],
        help_text="Только русские буквы"
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name="Фамилия",
        validators=[validate_russian_name],
        help_text="Только русские буквы"
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Email",
        help_text="example@school.ru"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Телефон",
        validators=[validate_phone_number],
        help_text="Формат: +7 123 456-78-90"
    )
    specialization = models.CharField(
        max_length=200,
        verbose_name="Специализация",
        help_text="Например: Программирование, Математика"
    )
    experience_years = models.IntegerField(
        verbose_name="Стаж (лет)",
        default=0,
        validators=[validate_experience_years, MinValueValidator(0), MaxValueValidator(50)],
        help_text="От 0 до 50 лет"
    )
    hire_date = models.DateField(
        verbose_name="Дата найма",
        null=True,
        blank=True
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен"
    )
    
    # НОВЫЕ ПОЛЯ
    degree = models.CharField(
        max_length=100,
        choices=[
            ('bachelor', 'Бакалавр'),
            ('master', 'Магистр'),
            ('phd', 'Кандидат наук'),
            ('doctor', 'Доктор наук'),
            ('professor', 'Профессор'),
        ],
        default='master',
        verbose_name="Ученая степень"
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="Рейтинг (0-5)"
    )
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Зарплата (руб)"
    )
    
    def __str__(self):
        return f"{self.last_name} {self.first_name}"
    
    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"
        ordering = ['last_name', 'first_name']


# ==================== МОДЕЛЬ TEACHERINFO ====================
class TeacherInfo(models.Model):
    """Дополнительная информация о преподавателе"""
    teacher = models.OneToOneField(
        Teacher,
        on_delete=models.CASCADE,
        related_name='info'
    )
    bio = models.TextField(
        blank=True,
        verbose_name="Биография"
    )
    education = models.CharField(
        max_length=300,
        verbose_name="Образование"
    )
    office_number = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Кабинет"
    )
    
    # НОВЫЕ ПОЛЯ
    awards = models.TextField(
        blank=True,
        verbose_name="Награды и достижения",
        help_text="Перечислите награды через запятую"
    )
    languages = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Иностранные языки",
        help_text="Например: Английский (C1), Французский (B2)"
    )
    projects_count = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Количество проектов"
    )
    
    def __str__(self):
        return f"Инфо о {self.teacher}"
    
    class Meta:
        verbose_name = "Информация о преподавателе"
        verbose_name_plural = "Информация о преподавателях"


# ==================== МОДЕЛЬ COURSE ====================
class Course(models.Model):
    """Курс"""
    title = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название",
        help_text="Уникальное название курса"
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Цена (руб)"
    )
    
    # НОВЫЕ ПОЛЯ
    level = models.CharField(
        max_length=50,
        choices=[
            ('beginner', 'Начинающий'),
            ('intermediate', 'Средний'),
            ('advanced', 'Продвинутый'),
            ('expert', 'Эксперт'),
        ],
        default='beginner',
        verbose_name="Уровень сложности"
    )
    duration_hours = models.IntegerField(
        default=40,
        validators=[MinValueValidator(1), MaxValueValidator(500)],
        verbose_name="Длительность (часов)"
    )
    max_students = models.IntegerField(
        default=30,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        verbose_name="Максимум студентов"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Курс активен"
    )
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


# ==================== МОДЕЛЬ STUDENT ====================
class Student(models.Model):
    """Студент"""
    first_name = models.CharField(
        max_length=50,
        verbose_name="Имя",
        validators=[validate_russian_name]
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name="Фамилия",
        validators=[validate_russian_name]
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Email"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[validate_phone_number],
        verbose_name="Телефон"
    )
    courses = models.ManyToManyField(
        Course,
        blank=True,
        related_name='students',
        verbose_name="Курсы"
    )
    
    # НОВЫЕ ПОЛЯ
    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Дата рождения"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен"
    )
    enrollment_date = models.DateField(
        auto_now_add=True,
        verbose_name="Дата регистрации"
    )
    
    def __str__(self):
        return f"{self.last_name} {self.first_name}"
    
    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"
        ordering = ['last_name', 'first_name']