from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя с дополнительными полями
    """
    email = models.EmailField('Email', unique=True)
    phone = models.CharField('Телефон', max_length=20, blank=True, null=True)
    birth_date = models.DateField('Дата рождения', blank=True, null=True)
    
    # Добавляем поле для аватарки
    avatar = models.ImageField(
        'Аватар', 
        upload_to='avatars/', 
        blank=True, 
        null=True,
        help_text='Загрузите изображение для аватара'
    )
    
    bio = models.TextField('О себе', max_length=500, blank=True, null=True)
    city = models.CharField('Город', max_length=100, blank=True, null=True)
    
    friends = models.ManyToManyField(
        'self',
        verbose_name='Друзья',
        symmetrical=True,
        blank=True
    )
    
    def __str__(self):
        return self.username
    
    def get_friends(self):
        return self.friends.all()
    
    def add_friend(self, user):
        if user != self and user not in self.friends.all():
            self.friends.add(user)
            return True
        return False
    
    def remove_friend(self, user):
        if user in self.friends.all():
            self.friends.remove(user)
            return True
        return False
    
    def is_friend(self, user):
        return self.friends.filter(id=user.id).exists()
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'