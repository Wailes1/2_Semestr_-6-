from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
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
        # Автоматически входим после регистрации
        login(self.request, self.object)
        return result

def home_view(request):
    """
    Главная страница
    """
    return render(request, 'base.html')