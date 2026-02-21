from django.db import models

class Teacher(models.Model):
    """Преподаватель"""
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    email = models.EmailField(unique=True, verbose_name="Email")
    specialization = models.CharField(max_length=200, verbose_name="Специализация")
    
    def __str__(self):
        return f"{self.last_name} {self.first_name}"
    
    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"


class TeacherInfo(models.Model):
    """Дополнительная информация о преподавателе (связь 1:1)"""
    teacher = models.OneToOneField(
        Teacher, 
        on_delete=models.CASCADE,  # ON DELETE CASCADE
        related_name='info'
    )
    bio = models.TextField(blank=True, verbose_name="Биография")
    education = models.CharField(max_length=200, verbose_name="Образование")
    office_number = models.CharField(max_length=20, blank=True, verbose_name="Кабинет")
    
    def __str__(self):
        return f"Инфо о {self.teacher}"
    
    class Meta:
        verbose_name = "Информация о преподавателе"
        verbose_name_plural = "Информация о преподавателях"


class Course(models.Model):
    """Курс (связь с Teacher 1:N)"""
    title = models.CharField(max_length=200, verbose_name="Название")
    teacher = models.ForeignKey(
        Teacher, 
        on_delete=models.SET_NULL,  # ON DELETE SET NULL
        null=True, 
        blank=True,
        related_name='courses'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Student(models.Model):
    """Студент (связь с Course N:N)"""
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    email = models.EmailField(unique=True, verbose_name="Email")
    courses = models.ManyToManyField(
        Course, 
        blank=True, 
        related_name='students',
        verbose_name="Курсы"
    )
    
    def __str__(self):
        return f"{self.last_name} {self.first_name}"
    
    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"