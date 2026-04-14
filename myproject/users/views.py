from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, Http404
from django.contrib import messages
from .forms import CustomUserCreationForm, UserProfileForm
from .models import CustomUser


class RegisterView(CreateView):
    """
    Представление для регистрации пользователя
    """
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        result = super().form_valid(form)
        # Автоматически логиним пользователя после регистрации
        login(self.request, self.object)
        messages.success(self.request, f'Добро пожаловать, {self.object.username}!')
        return result


class ProfileView(LoginRequiredMixin, DetailView):
    """
    Просмотр профиля пользователя
    """
    model = CustomUser
    template_name = 'users/profile.html'
    context_object_name = 'profile_user'
    
    def dispatch(self, request, *args, **kwargs):
        """Проверка прав доступа"""
        username = kwargs.get('username')
        self.profile_user = get_object_or_404(CustomUser, username=username)
        
        if request.user.is_authenticated:
            # Своя страница - можно
            if request.user == self.profile_user:
                return super().dispatch(request, *args, **kwargs)
            
            # Страница друга - можно
            if request.user.is_friend(self.profile_user):
                return super().dispatch(request, *args, **kwargs)
            
            # Страница незнакомца - нельзя
            messages.error(request, 'Вы можете просматривать только страницы своих друзей!')
            return redirect('users:user_list')
        
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
    Редактирование профиля пользователя
    """
    model = CustomUser
    form_class = UserProfileForm
    template_name = 'users/profile_edit.html'
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Профиль успешно обновлен!')
        return super().form_valid(form)
    
    def get_success_url(self):
        # Перенаправляем на страницу профиля после редактирования
        return reverse_lazy('users:profile', kwargs={'username': self.request.user.username})


class UserListView(LoginRequiredMixin, ListView):
    """
    Список всех пользователей (только для авторизованных)
    """
    model = CustomUser
    template_name = 'users/user_list.html'
    context_object_name = 'users'
    paginate_by = 20
    
    def get_queryset(self):
        # Важно: добавляем сортировку для корректной пагинации
        return CustomUser.objects.exclude(id=self.request.user.id).order_by('username')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for user in context['users']:
            user.is_friend = self.request.user.is_friend(user)
        return context


@login_required
def add_friend(request, user_id):
    """
    Добавление друга
    """
    if request.method == 'POST':
        user_to_add = get_object_or_404(CustomUser, id=user_id)
        
        if user_to_add == request.user:
            messages.error(request, 'Нельзя добавить самого себя в друзья')
            return redirect('users:user_list')
        
        if request.user.add_friend(user_to_add):
            messages.success(request, f'{user_to_add.username} добавлен в друзья!')
        else:
            messages.info(request, f'{user_to_add.username} уже в друзьях')
        
        next_url = request.POST.get('next', 'users:user_list')
        return redirect(next_url)
    
    return redirect('users:user_list')


@login_required
def remove_friend(request, user_id):
    """
    Удаление из друзей
    """
    if request.method == 'POST':
        user_to_remove = get_object_or_404(CustomUser, id=user_id)
        
        if request.user.remove_friend(user_to_remove):
            messages.success(request, f'{user_to_remove.username} удален из друзей')
        else:
            messages.error(request, 'Ошибка при удалении')
        
        next_url = request.POST.get('next', 'users:user_list')
        return redirect(next_url)
    
    return redirect('users:user_list')


def home_view(request):
    """
    Главная страница
    """
    return render(request, 'base.html')