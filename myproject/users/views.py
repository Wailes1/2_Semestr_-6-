import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import CustomUserCreationForm, UserProfileForm
from .models import CustomUser

# Создаем логгер для модуля
logger = logging.getLogger(__name__)


class CustomLoginView(LoginView):
    """Кастомное представление входа с логированием"""
    
    def form_valid(self, form):
        """Успешный вход"""
        username = form.cleaned_data.get('username')
        logger.info(f"User '{username}' logged in successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Неудачный вход"""
        username = form.cleaned_data.get('username', 'unknown')
        logger.warning(f"Failed login attempt for user '{username}' - invalid credentials")
        return super().form_invalid(form)


class RegisterView(CreateView):
    """
    Представление для регистрации пользователя
    """
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        logger.info(f"New user registered: '{self.object.username}' (email: {self.object.email})")
        login(self.request, self.object)
        messages.success(self.request, f'Добро пожаловать, {self.object.username}!')
        return response
    
    def form_invalid(self, form):
        errors = dict(form.errors)
        username = form.cleaned_data.get('username', 'unknown')
        logger.warning(f"Registration failed for '{username}': {errors}")
        return super().form_invalid(form)


class ProfileView(LoginRequiredMixin, DetailView):
    """
    Просмотр профиля пользователя
    """
    model = CustomUser
    template_name = 'users/profile.html'
    context_object_name = 'profile_user'
    
    def dispatch(self, request, *args, **kwargs):
        username = kwargs.get('username')
        self.profile_user = get_object_or_404(CustomUser, username=username)
        
        if request.user.is_authenticated:
            if request.user == self.profile_user:
                logger.debug(f"User '{request.user.username}' viewed own profile")
                return super().dispatch(request, *args, **kwargs)
            
            if request.user.is_friend(self.profile_user):
                logger.debug(f"User '{request.user.username}' viewed friend '{self.profile_user.username}' profile")
                return super().dispatch(request, *args, **kwargs)
            
            logger.warning(f"User '{request.user.username}' attempted to view non-friend '{self.profile_user.username}' profile - ACCESS DENIED")
            messages.error(request, 'Вы можете просматривать только страницы своих друзей!')
            return redirect('users:user_list')
        
        logger.warning(f"Anonymous user attempted to view profile '{username}' - REDIRECTED TO LOGIN")
        messages.error(request, 'Пожалуйста, войдите в систему')
        return redirect('login')
    
    def get_object(self):
        return self.profile_user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_own_profile'] = (self.request.user == self.profile_user)
        context['is_friend'] = self.request.user.is_friend(self.profile_user)
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """
    Редактирование профиля пользователя с логированием загрузки аватарки
    """
    model = CustomUser
    form_class = UserProfileForm
    template_name = 'users/profile_edit.html'
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        logger.info(f"User '{self.request.user.username}' updated profile successfully")
        messages.success(self.request, 'Профиль успешно обновлен!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        errors = dict(form.errors)
        # ИЗМЕНИЛ: warning → error
        logger.error(f"User '{self.request.user.username}' failed to update profile. Errors: {errors}")
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме')
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'username': self.request.user.username})

class UserListView(LoginRequiredMixin, ListView):
    """
    Список всех пользователей
    """
    model = CustomUser
    template_name = 'users/user_list.html'
    context_object_name = 'users'
    paginate_by = 20
    
    def get_queryset(self):
        logger.debug(f"User '{self.request.user.username}' requested user list")
        return CustomUser.objects.exclude(id=self.request.user.id).order_by('username')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for user in context['users']:
            user.is_friend = self.request.user.is_friend(user)
        return context


@login_required
def add_friend(request, user_id):
    """
    Добавление друга с логированием
    """
    if request.method == 'POST':
        user_to_add = get_object_or_404(CustomUser, id=user_id)
        
        if user_to_add == request.user:
            logger.warning(f"User '{request.user.username}' attempted to add themselves as friend")
            messages.error(request, 'Нельзя добавить самого себя в друзья')
            return redirect('users:user_list')
        
        if request.user.add_friend(user_to_add):
            logger.info(f"User '{request.user.username}' added '{user_to_add.username}' as friend")
            messages.success(request, f'{user_to_add.username} добавлен в друзья!')
        else:
            logger.info(f"User '{request.user.username}' attempted to add '{user_to_add.username}' but already friends")
            messages.info(request, f'{user_to_add.username} уже в друзьях')
        
        next_url = request.POST.get('next', 'users:user_list')
        return redirect(next_url)
    
    return redirect('users:user_list')


@login_required
def remove_friend(request, user_id):
    """
    Удаление из друзей с логированием
    """
    if request.method == 'POST':
        user_to_remove = get_object_or_404(CustomUser, id=user_id)
        
        if request.user.remove_friend(user_to_remove):
            logger.info(f"User '{request.user.username}' removed '{user_to_remove.username}' from friends")
            messages.success(request, f'{user_to_remove.username} удален из друзей')
        else:
            logger.warning(f"User '{request.user.username}' attempted to remove '{user_to_remove.username}' but not in friends")
            messages.error(request, 'Ошибка при удалении')
        
        next_url = request.POST.get('next', 'users:user_list')
        return redirect(next_url)
    
    return redirect('users:user_list')


def home_view(request):
    """
    Главная страница
    """
    user_status = request.user.username if request.user.is_authenticated else 'anonymous'
    logger.debug(f"Home page accessed by user: {user_status}")
    return render(request, 'base.html')