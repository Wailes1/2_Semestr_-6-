from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import Http404
from .data import COURSES, AUTHORS

def index(request):
    """Главная страница"""
    return render(request, 'index.html')

def courses(request):
    """Список всех курсов"""
    return render(request, 'courses.html', {'courses': COURSES})

def course_detail(request, course_id):
    """Страница конкретного курса"""
    # Ищем курс по ID
    course = None
    for c in COURSES:
        if c['id'] == course_id:
            course = c
            break
    
    if not course:
        # Если курс не найден, показываем страницу 404
        return render(request, 'not_found.html', status=404)
    
    return render(request, 'course_detail.html', {'course': course})

def authors(request):
    """Список всех авторов"""
    return render(request, 'authors.html', {'authors': AUTHORS})

def author_details(request, author_id):
    """Страница конкретного автора"""
    # Ищем автора по ID
    author = None
    for a in AUTHORS:
        if a['id'] == author_id:
            author = a
            break
    
    if not author:
        # Если автор не найден, показываем страницу 404
        return render(request, 'not_found.html', status=404)
    
    return render(request, 'author_details.html', {
        'author': author,
        'COURSES': COURSES  # Передаем курсы в шаблон
    })

def info(request):
    """Страница информации о сайте"""
    return render(request, 'info.html')

def not_found(request):
    """Страница 404 (не найдено)"""
    return render(request, 'not_found.html', status=404)