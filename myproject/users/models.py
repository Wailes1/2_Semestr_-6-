from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя с дополнительными полями
    """
    # Задание 1: Добавить email и номер телефона
    email = models.EmailField('Email', unique=True)  # email уже есть, делаем уникальным
    phone = models.CharField('Телефон', max_length=20, blank=True, null=True)
    birth_date = models.DateField('Дата рождения', blank=True, null=True)
    
    # Дополнительные поля для соцсети
    avatar = models.ImageField('Аватар', upload_to='avatars/', blank=True, null=True)
    bio = models.TextField('О себе', max_length=500, blank=True, null=True)
    city = models.CharField('Город', max_length=100, blank=True, null=True)
    
    # Поле для друзей (многие ко многим)
    friends = models.ManyToManyField(
        'self',
        verbose_name='Друзья',
        symmetrical=True,  # Если A друг B, то B друг A
        blank=True
    )
    
    def __str__(self):
        return self.username
    
    def get_friends(self):
        """Получить список друзей"""
        return self.friends.all()
    
    def add_friend(self, user):
        """Добавить друга"""
        if user != self and user not in self.friends.all():
            self.friends.add(user)
            return True
        return False
    
    def remove_friend(self, user):
        """Удалить друга"""
        if user in self.friends.all():
            self.friends.remove(user)
            return True
        return False
    
    def is_friend(self, user):
        """Проверить, является ли пользователь другом"""
        return self.friends.filter(id=user.id).exists()
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

