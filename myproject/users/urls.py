from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    RegisterView, ProfileView, ProfileEditView, 
    UserListView, add_friend, remove_friend
)

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/edit/', ProfileEditView.as_view(), name='profile_edit'), 
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('add_friend/<int:user_id>/', add_friend, name='add_friend'),
    path('remove_friend/<int:user_id>/', remove_friend, name='remove_friend'),
]