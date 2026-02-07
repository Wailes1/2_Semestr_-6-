from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('courses/', views.courses, name='courses'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('authors/', views.authors, name='authors'),
    path('authors/<int:author_id>/', views.author_details, name='author_details'),
    path('info/', views.info, name='info'),
    path('not_found/', views.not_found, name='not_found'),
    re_path(r'^.*$', views.not_found),
]
