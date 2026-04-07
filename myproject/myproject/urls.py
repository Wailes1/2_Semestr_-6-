from django.contrib import admin
from django.urls import path, include
from users.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    # Стандартные URL из django.contrib.auth
    path('auth/', include('django.contrib.auth.urls')),
    # URL для регистрации
    path('auth/', include('users.urls')),
]