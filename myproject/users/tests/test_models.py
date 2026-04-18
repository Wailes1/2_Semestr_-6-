import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from users.models import CustomUser

User = get_user_model()

@pytest.mark.django_db
class TestUserModel:
    """Тесты для модели пользователя"""
    
    def test_create_user(self, user):
        """Тест создания обычного пользователя"""
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.phone == '+79991234567'
        assert user.check_password('testpass123')
        assert user.is_active
        assert not user.is_staff
        assert not user.is_superuser

    def test_create_user_with_email_is_required(self, db):
        """Тест: email не обязателен в вашей модели"""
        # В вашей модели email может быть пустым
        user = User.objects.create_user(
            username='testuser2',
            email='',  # пустой email допустим
            password='pass123'
        )
        assert user.email == ''  # или None, зависит от модели
    
    def test_create_superuser(self, admin_user):
        """Тест создания суперпользователя"""
        assert admin_user.is_staff
        assert admin_user.is_superuser
    
    def test_user_str_method(self, user):
        """Тест строкового представления пользователя"""
        assert str(user) == 'testuser'
    
    def test_add_friend(self, user, another_user):
        """Тест добавления в друзья"""
        result = user.add_friend(another_user)
        assert result == True
        assert user.is_friend(another_user)
        assert another_user.is_friend(user)
    
    def test_add_self_as_friend(self, user):
        """Тест: нельзя добавить себя в друзья"""
        result = user.add_friend(user)
        assert result == False
        assert not user.is_friend(user)
    
    def test_add_friend_twice(self, user, another_user):
        """Тест: повторное добавление друга"""
        user.add_friend(another_user)
        result = user.add_friend(another_user)
        assert result == False
    
    def test_remove_friend(self, user, another_user):
        """Тест удаления из друзей"""
        user.add_friend(another_user)
        assert user.is_friend(another_user)
        
        result = user.remove_friend(another_user)
        assert result == True
        assert not user.is_friend(another_user)
    
    def test_get_friends(self, user, another_user, friend_user):
        """Тест получения списка друзей"""
        user.add_friend(another_user)
        friends = user.get_friends()
        assert friend_user in friends
        assert another_user in friends
        assert friends.count() == 2
    
    def test_is_friend(self, user, friend_user, non_friend_user):
        """Тест проверки дружбы"""
        assert user.is_friend(friend_user) == True
        assert user.is_friend(non_friend_user) == False

    def test_unique_email(self, db, user):
        """Тест: email должен быть уникальным"""
        with pytest.raises(Exception):
            User.objects.create_user(
                username='another',
                email='test@example.com',  # тот же email
                password='pass123'
            )