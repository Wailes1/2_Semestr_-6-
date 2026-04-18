import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from users.models import CustomUser

User = get_user_model()

@pytest.fixture
def client():
    """Фикстура для HTTP клиента"""
    return Client()

@pytest.fixture
def user(db):
    """Фикстура для создания обычного пользователя"""
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        phone='+79991234567'
    )
    return user

@pytest.fixture
def another_user(db):
    """Фикстура для создания другого пользователя"""
    user = User.objects.create_user(
        username='anotheruser',
        email='another@example.com',
        password='testpass123',
        phone='+79997654321'
    )
    return user

@pytest.fixture
def admin_user(db):
    """Фикстура для создания администратора"""
    user = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass123'
    )
    return user

@pytest.fixture
def authenticated_client(client, user):
    """Фикстура для аутентифицированного клиента"""
    client.login(username='testuser', password='testpass123')
    return client

@pytest.fixture
def friend_user(db, user):
    """Фикстура для пользователя-друга"""
    friend = User.objects.create_user(
        username='frienduser',
        email='friend@example.com',
        password='friendpass123'
    )
    # Добавляем в друзья
    user.friends.add(friend)
    friend.friends.add(user)
    return friend

@pytest.fixture
def non_friend_user(db):
    """Фикстура для пользователя, не являющегося другом"""
    return User.objects.create_user(
        username='nonfriend',
        email='nonfriend@example.com',
        password='nonfriend123'
    )

@pytest.fixture
def user_data():
    """Фикстура с данными для регистрации"""
    return {
        'username': 'newuser',
        'email': 'new@example.com',
        'password1': 'StrongPass123!',
        'password2': 'StrongPass123!',
        'phone': '+79998887766',
        'birth_date': '1990-01-01'
    }

@pytest.fixture
def invalid_user_data():
    """Фикстура с невалидными данными"""
    return {
        'username': 'testuser',  # уже существует
        'email': 'invalid-email',  # невалидный email
        'password1': '123',  # слишком короткий
        'password2': '456',  # не совпадает
    }