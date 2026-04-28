from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    CustomLoginView,  # Используем кастомный вместо стандартного
    RegisterView, 
    ProfileView, 
    ProfileEditView, 
    UserListView, 
    add_friend, 
    remove_friend, 
    home_view
)

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),  # Кастомный login
    path('profile/edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('add_friend/<int:user_id>/', add_friend, name='add_friend'),
    path('remove_friend/<int:user_id>/', remove_friend, name='remove_friend'),
]

# Для медиафайлов
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)