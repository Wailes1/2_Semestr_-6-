import pytest
from django.urls import reverse, resolve
from users.views import (
    RegisterView, ProfileView, ProfileEditView,
    UserListView, add_friend, remove_friend, home_view
)

@pytest.mark.django_db
class TestUrls:
    """Тесты URL маршрутов"""
    
    def test_home_url(self):
        """Тест: главная страница"""
        url = reverse('home')
        assert url == '/'
        resolver = resolve(url)
        assert resolver.func == home_view
    
    def test_register_url(self):
        """Тест: URL регистрации"""
        url = reverse('users:register')
        assert url == '/auth/register/'
        resolver = resolve(url)
        assert resolver.func.view_class == RegisterView
    
    def test_profile_url(self):
        """Тест: URL профиля"""
        url = reverse('users:profile', kwargs={'username': 'testuser'})
        assert url == '/auth/profile/testuser/'
        resolver = resolve(url)
        assert resolver.func.view_class == ProfileView
    
    def test_profile_edit_url(self):
        """Тест: URL редактирования профиля"""
        url = reverse('users:profile_edit')
        assert url == '/auth/profile/edit/'
        resolver = resolve(url)
        assert resolver.func.view_class == ProfileEditView
    
    def test_user_list_url(self):
        """Тест: URL списка пользователей"""
        url = reverse('users:user_list')
        assert url == '/auth/users/'
        resolver = resolve(url)
        assert resolver.func.view_class == UserListView
    
    def test_login_url(self):
        """Тест: URL входа"""
        url = reverse('login')
        assert url == '/auth/login/'
    
    def test_logout_url(self):
        """Тест: URL выхода"""
        url = reverse('logout')
        assert url == '/auth/logout/'
    
    def test_password_change_url(self):
        """Тест: URL смены пароля"""
        url = reverse('password_change')
        assert url == '/auth/password_change/'
    
    def test_password_reset_url(self):
        """Тест: URL восстановления пароля"""
        url = reverse('password_reset')
        assert url == '/auth/password_reset/'
    
    def test_add_friend_url(self):
        """Тест: URL добавления друга"""
        url = reverse('users:add_friend', kwargs={'user_id': 1})
        assert url == '/auth/add_friend/1/'
        resolver = resolve(url)
        assert resolver.func == add_friend
    
    def test_remove_friend_url(self):
        """Тест: URL удаления друга"""
        url = reverse('users:remove_friend', kwargs={'user_id': 1})
        assert url == '/auth/remove_friend/1/'
        resolver = resolve(url)
        assert resolver.func == remove_friend