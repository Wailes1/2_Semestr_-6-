import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.models import CustomUser

User = get_user_model()

@pytest.mark.django_db
class TestRegistrationView:
    """Тесты регистрации"""
    
    def test_registration_page_status(self, client):
        """Тест: страница регистрации доступна"""
        url = reverse('users:register')
        response = client.get(url)
        assert response.status_code == 200
    
    def test_registration_success(self, client, user_data):
        """Тест: успешная регистрация"""
        url = reverse('users:register')
        response = client.post(url, user_data)
        # Проверка редиректа после успешной регистрации
        assert response.status_code == 302
        assert response.url == reverse('home')
        
        # Проверка создания пользователя
        assert User.objects.filter(username='newuser').exists()
        new_user = User.objects.get(username='newuser')
        assert new_user.email == 'new@example.com'
    
    def test_registration_failure_duplicate(self, client, user, user_data):
        """Тест: ошибка при дублировании пользователя"""
        user_data['username'] = 'testuser'  # уже существует
        url = reverse('users:register')
        response = client.post(url, user_data)
        assert response.status_code == 200  # возвращаемся на страницу с ошибкой
        assert 'username' in response.context['form'].errors
    
    def test_auto_login_after_registration(self, client, user_data):
        """Тест: автоматический вход после регистрации"""
        url = reverse('users:register')
        response = client.post(url, user_data)
        # Проверяем, что пользователь аутентифицирован
        assert response.wsgi_request.user.is_authenticated


@pytest.mark.django_db
class TestLoginLogoutView:
    """Тесты входа и выхода"""
    
    def test_login_page_status(self, client):
        """Тест: страница входа доступна"""
        url = reverse('login')
        response = client.get(url)
        assert response.status_code == 200
    
    def test_login_success(self, client, user):
        """Тест: успешный вход"""
        url = reverse('login')
        response = client.post(url, {
            'username': 'testuser',
            'password': 'testpass123'
        })
        assert response.status_code == 302
        assert response.url == reverse('home')
        # Проверка, что пользователь вошел
        assert response.wsgi_request.user.is_authenticated
    
    def test_login_failure_wrong_password(self, client, user):
        """Тест: неверный пароль"""
        url = reverse('login')
        response = client.post(url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        assert response.status_code == 200  # возвращаемся на страницу входа
        assert not response.wsgi_request.user.is_authenticated
    
    def test_login_failure_nonexistent_user(self, client):
        """Тест: несуществующий пользователь"""
        url = reverse('login')
        response = client.post(url, {
            'username': 'nonexistent',
            'password': 'somepass'
        })
        assert response.status_code == 200
        assert not response.wsgi_request.user.is_authenticated
    
    def test_logout_requires_post(self, authenticated_client):
        """Тест: выход требует POST запрос"""
        url = reverse('logout')
        response = authenticated_client.get(url)
        assert response.status_code == 405  # Method Not Allowed
    
    def test_logout_success(self, authenticated_client):
        """Тест: успешный выход"""
        url = reverse('logout')
        response = authenticated_client.post(url)
        assert response.status_code == 302
        assert response.url == reverse('home')
        assert not response.wsgi_request.user.is_authenticated


@pytest.mark.django_db
class TestProfileAccess:
    """Тесты проверки доступа к профилю (permissions)"""
    
    def test_own_profile_accessible(self, authenticated_client, user):
        """Тест: свой профиль доступен"""
        url = reverse('users:profile', kwargs={'username': user.username})
        response = authenticated_client.get(url)
        assert response.status_code == 200
    
    def test_friend_profile_accessible(self, authenticated_client, friend_user):
        """Тест: профиль друга доступен"""
        url = reverse('users:profile', kwargs={'username': friend_user.username})
        response = authenticated_client.get(url)
        assert response.status_code == 200
    
    def test_non_friend_profile_inaccessible(self, authenticated_client, non_friend_user):
        """Тест: профиль незнакомца недоступен"""
        url = reverse('users:profile', kwargs={'username': non_friend_user.username})
        response = authenticated_client.get(url)
        # Должен быть редирект или 403
        assert response.status_code == 302
    
    def test_anonymous_cannot_view_profile(self, client, user):
        """Тест: анонимный пользователь не может смотреть профиль"""
        url = reverse('users:profile', kwargs={'username': user.username})
        response = client.get(url)
        # Должен быть редирект на страницу входа
        assert response.status_code == 302
        assert response.url.startswith(reverse('login'))
    
    def test_anonymous_cannot_view_user_list(self, client):
        """Тест: анонимный пользователь не может смотреть список пользователей"""
        url = reverse('users:user_list')
        response = client.get(url)
        assert response.status_code == 302
        assert response.url.startswith(reverse('login'))
    
    def test_authenticated_can_view_user_list(self, authenticated_client):
        """Тест: авторизованный пользователь может смотреть список"""
        url = reverse('users:user_list')
        response = authenticated_client.get(url)
        assert response.status_code == 200


@pytest.mark.django_db
class TestProfileEdit:
    """Тесты редактирования профиля"""
    
    def test_profile_edit_page_accessible(self, authenticated_client):
        """Тест: страница редактирования доступна авторизованному"""
        url = reverse('users:profile_edit')
        response = authenticated_client.get(url)
        assert response.status_code == 200
    
    def test_profile_edit_page_inaccessible_for_anonymous(self, client):
        """Тест: страница редактирования недоступна анониму"""
        url = reverse('users:profile_edit')
        response = client.get(url)
        assert response.status_code == 302
    
    def test_profile_edit_success(self, authenticated_client, user):
        """Тест: успешное редактирование профиля"""
        url = reverse('users:profile_edit')
        response = authenticated_client.post(url, {
            'username': 'updatedname',
            'email': 'updated@example.com',
            'phone': '+79990001122',
            'bio': 'New bio',
            'city': 'Saint Petersburg'
        })
        assert response.status_code == 302
        # Проверяем редирект на профиль
        assert response.url == reverse('users:profile', kwargs={'username': 'updatedname'})
        
        # Проверяем обновление данных
        user.refresh_from_db()
        assert user.username == 'updatedname'
        assert user.email == 'updated@example.com'
        assert user.bio == 'New bio'


@pytest.mark.django_db
class TestFriendActions:
    """Тесты действий с друзьями"""
    
    def test_add_friend_success(self, authenticated_client, user, non_friend_user):
        """Тест: успешное добавление в друзья"""
        url = reverse('users:add_friend', kwargs={'user_id': non_friend_user.id})
        response = authenticated_client.post(url, {'next': reverse('users:user_list')})
        assert response.status_code == 302
        assert user.is_friend(non_friend_user)
    
    def test_add_self_as_friend(self, authenticated_client, user):
        """Тест: нельзя добавить себя в друзья"""
        url = reverse('users:add_friend', kwargs={'user_id': user.id})
        response = authenticated_client.post(url, {'next': reverse('users:user_list')})
        assert response.status_code == 302
        assert not user.is_friend(user)
    
    def test_add_friend_twice(self, authenticated_client, user, friend_user):
        """Тест: повторное добавление друга"""
        url = reverse('users:add_friend', kwargs={'user_id': friend_user.id})
        response = authenticated_client.post(url, {'next': reverse('users:user_list')})
        assert response.status_code == 302
        # Друг уже есть в друзьях
    
    def test_remove_friend_success(self, authenticated_client, user, friend_user):
        """Тест: успешное удаление из друзей"""
        assert user.is_friend(friend_user)
        url = reverse('users:remove_friend', kwargs={'user_id': friend_user.id})
        response = authenticated_client.post(url, {'next': reverse('users:user_list')})
        assert response.status_code == 302
        assert not user.is_friend(friend_user)
    
    def test_add_friend_unauthenticated(self, client, non_friend_user):
        """Тест: неавторизованный не может добавить друга"""
        url = reverse('users:add_friend', kwargs={'user_id': non_friend_user.id})
        response = client.post(url)
        assert response.status_code == 302
        assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
class TestRedirects:
    """Тесты редиректов (assertRedirects)"""
    
    def test_register_redirect_after_success(self, client, user_data):
        """Тест: редирект после успешной регистрации"""
        url = reverse('users:register')
        response = client.post(url, user_data)
        assert response.status_code == 302
        assert response.url == reverse('home')
    
    def test_login_redirect_after_success(self, client, user):
        """Тест: редирект после успешного входа"""
        url = reverse('login')
        response = client.post(url, {
            'username': 'testuser',
            'password': 'testpass123'
        })
        assert response.status_code == 302
        assert response.url == reverse('home')
    
    def test_logout_redirect_after_success(self, authenticated_client):
        """Тест: редирект после выхода"""
        url = reverse('logout')
        response = authenticated_client.post(url)
        assert response.status_code == 302
        assert response.url == reverse('home')
    
    def test_profile_edit_redirect_to_profile(self, authenticated_client, user):
        """Тест: редирект на профиль после редактирования"""
        url = reverse('users:profile_edit')
        response = authenticated_client.post(url, {
            'username': 'testuser',
            'email': 'test@example.com',
        })
        assert response.status_code == 302
        assert response.url == reverse('users:profile', kwargs={'username': 'testuser'})
    
    def test_anonymous_redirect_to_login(self, client, user):
        """Тест: аноним редиректится на логин"""
        url = reverse('users:profile', kwargs={'username': user.username})
        response = client.get(url)
        assert response.status_code == 302
        assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
class TestErrorHandling:
    """Тестирование ошибок"""
    
    def test_404_for_nonexistent_profile(self, authenticated_client):
        """Тест: 404 для несуществующего профиля"""
        url = reverse('users:profile', kwargs={'username': 'nonexistentuser'})
        response = authenticated_client.get(url)
        assert response.status_code == 404
    
    def test_404_for_nonexistent_user_in_friend_action(self, authenticated_client):
        """Тест: 404 при добавлении несуществующего пользователя"""
        url = reverse('users:add_friend', kwargs={'user_id': 99999})
        response = authenticated_client.post(url)
        assert response.status_code == 404
    
    def test_form_validation_errors_displayed(self, client):
        """Тест: отображение ошибок валидации"""
        url = reverse('users:register')
        response = client.post(url, {
            'username': '',
            'email': 'invalid',
            'password1': '123',
            'password2': '456'
        })
        assert response.status_code == 200
        form = response.context.get('form')
        assert form is not None
        assert form.errors
        assert 'username' in form.errors or 'email' in form.errors