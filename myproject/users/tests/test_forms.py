import pytest
from users.forms import CustomUserCreationForm, UserProfileForm
from users.models import CustomUser

@pytest.mark.django_db
class TestRegistrationForm:
    """Тесты формы регистрации"""
    
    def test_valid_form(self, user_data):
        """Тест валидной формы"""
        form = CustomUserCreationForm(data=user_data)
        assert form.is_valid()
    
    def test_invalid_form_missing_username(self, user_data):
        """Тест: отсутствует имя пользователя"""
        user_data['username'] = ''
        form = CustomUserCreationForm(data=user_data)
        assert not form.is_valid()
        assert 'username' in form.errors
    
    def test_invalid_form_duplicate_username(self, user, user_data):
        """Тест: дублирование имени пользователя"""
        user_data['username'] = 'testuser'  # уже существует
        form = CustomUserCreationForm(data=user_data)
        assert not form.is_valid()
    
    def test_invalid_form_duplicate_email(self, user, user_data):
        """Тест: дублирование email"""
        user_data['email'] = 'test@example.com'  # уже существует
        form = CustomUserCreationForm(data=user_data)
        assert not form.is_valid()
        assert 'email' in form.errors
    
    def test_invalid_form_passwords_mismatch(self, user_data):
        """Тест: пароли не совпадают"""
        user_data['password2'] = 'differentpass'
        form = CustomUserCreationForm(data=user_data)
        assert not form.is_valid()
        assert 'password2' in form.errors
    
    def test_invalid_form_weak_password(self, user_data):
        """Тест: слишком слабый пароль"""
        user_data['password1'] = '123'
        user_data['password2'] = '123'
        form = CustomUserCreationForm(data=user_data)
        assert not form.is_valid()
    
    def test_invalid_email_format(self, user_data):
        """Тест: невалидный формат email"""
        user_data['email'] = 'invalid-email'
        form = CustomUserCreationForm(data=user_data)
        assert not form.is_valid()
    
    @pytest.mark.parametrize('field,value,should_be_valid', [
        ('username', 'validuser', True),
        ('username', 'a', True),  # ИЗМЕНИЛ: теперь True, т.к. Django допускает 1 символ
        ('username', 'a' * 151, False),  # 151 символ - слишком длинный
        ('email', 'test@example.com', True),
        ('email', 'invalid', False),
        ('phone', '+79991234567', True),
        ('phone', '123', True),
    ])
    def test_form_field_validation(self, user_data, field, value, should_be_valid):
        """Параметризованный тест полей формы"""
        user_data[field] = value
        form = CustomUserCreationForm(data=user_data)
        if should_be_valid:
            assert form.is_valid() or field not in form.errors
        else:
            assert not form.is_valid() or field in form.errors


@pytest.mark.django_db
class TestProfileForm:
    """Тесты формы профиля"""
    
    def test_valid_profile_form(self, user):
        """Тест валидной формы профиля"""
        form = UserProfileForm(instance=user, data={
            'username': 'updateduser',
            'email': 'updated@example.com',
            'phone': '+79991112233',
            'bio': 'This is my bio',
            'city': 'Moscow'
        })
        assert form.is_valid()
    
    def test_profile_form_duplicate_email(self, user, another_user):
        """Тест: дублирование email в профиле"""
        form = UserProfileForm(instance=user, data={
            'username': 'testuser',
            'email': 'another@example.com',  # email другого пользователя
        })
        assert not form.is_valid()
        assert 'email' in form.errors