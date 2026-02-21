from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Teacher, TeacherInfo, Course, Student


# ==================== ГЛАВНАЯ ====================
def index(request):
    """Главная страница"""
    teachers_count = Teacher.objects.count()
    courses_count = Course.objects.count()
    students_count = Student.objects.count()
    
    return render(request, 'schedule/index.html', {
        'teachers_count': teachers_count,
        'courses_count': courses_count,
        'students_count': students_count,
    })


# ==================== TEACHER (ПРЕПОДАВАТЕЛИ) ====================

from django.db.models import Count

def teacher_list(request):
    """Список всех преподавателей с фильтром по количеству курсов"""
    teachers = Teacher.objects.annotate(
        course_count=Count('courses')
    )
    
    # Фильтр по минимальному количеству курсов
    min_courses = request.GET.get('min_courses')
    if min_courses:
        teachers = teachers.filter(course_count__gte=int(min_courses))
    
    return render(request, 'schedule/teacher_list.html', {
        'teachers': teachers,
        'min_courses': min_courses
    })


def teacher_detail(request, teacher_id):
    """Детальная страница преподавателя"""
    teacher = get_object_or_404(Teacher, id=teacher_id)
    return render(request, 'schedule/teacher_detail.html', {'teacher': teacher})


def teacher_create(request):
    """Создание преподавателя"""
    if request.method == 'POST':
        # Создаем преподавателя
        teacher = Teacher.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            specialization=request.POST['specialization']
        )
        # Создаем дополнительную информацию
        TeacherInfo.objects.create(
            teacher=teacher,
            bio=request.POST.get('bio', ''),
            education=request.POST.get('education', ''),
            office_number=request.POST.get('office_number', '')
        )
        messages.success(request, 'Преподаватель создан!')
        return redirect('teacher_detail', teacher_id=teacher.id)
    
    return render(request, 'schedule/teacher_form.html')


def teacher_update(request, teacher_id):
    """Редактирование преподавателя"""
    teacher = get_object_or_404(Teacher, id=teacher_id)
    
    if request.method == 'POST':
        # Обновляем преподавателя
        teacher.first_name = request.POST['first_name']
        teacher.last_name = request.POST['last_name']
        teacher.email = request.POST['email']
        teacher.specialization = request.POST['specialization']
        teacher.save()
        
        # Обновляем или создаем информацию
        info, created = TeacherInfo.objects.get_or_create(teacher=teacher)
        info.bio = request.POST.get('bio', '')
        info.education = request.POST.get('education', '')
        info.office_number = request.POST.get('office_number', '')
        info.save()
        
        messages.success(request, 'Данные обновлены!')
        return redirect('teacher_detail', teacher_id=teacher.id)
    
    return render(request, 'schedule/teacher_form.html', {'teacher': teacher})


def teacher_delete(request, teacher_id):
    """Удаление преподавателя"""
    teacher = get_object_or_404(Teacher, id=teacher_id)
    
    if request.method == 'POST':
        teacher.delete()
        messages.success(request, 'Преподаватель удален!')
        return redirect('teacher_list')
    
    return render(request, 'schedule/teacher_confirm_delete.html', {'teacher': teacher})


# ==================== COURSE (КУРСЫ) ====================

def course_list(request):
    """Список всех курсов"""
    courses = Course.objects.all()
    return render(request, 'schedule/course_list.html', {'courses': courses})


def course_detail(request, course_id):
    """Детальная страница курса"""
    course = get_object_or_404(Course, id=course_id)
    students = course.students.all()
    return render(request, 'schedule/course_detail.html', {
        'course': course,
        'students': students
    })


def course_create(request):
    """Создание курса"""
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher')
        teacher = Teacher.objects.get(id=teacher_id) if teacher_id else None
        
        course = Course.objects.create(
            title=request.POST['title'],
            price=request.POST['price'],
            teacher=teacher
        )
        messages.success(request, 'Курс создан!')
        return redirect('course_detail', course_id=course.id)
    
    teachers = Teacher.objects.all()
    return render(request, 'schedule/course_form.html', {'teachers': teachers})


def course_update(request, course_id):
    """Редактирование курса"""
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher')
        
        course.title = request.POST['title']
        course.price = request.POST['price']
        course.teacher = Teacher.objects.get(id=teacher_id) if teacher_id else None
        course.save()
        
        messages.success(request, 'Курс обновлен!')
        return redirect('course_detail', course_id=course.id)
    
    teachers = Teacher.objects.all()
    return render(request, 'schedule/course_form.html', {
        'course': course,
        'teachers': teachers
    })


def course_delete(request, course_id):
    """Удаление курса"""
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Курс удален!')
        return redirect('course_list')
    
    return render(request, 'schedule/course_confirm_delete.html', {'course': course})


# ==================== STUDENT (СТУДЕНТЫ) ====================

from django.db.models import Count

def student_list(request):
    """Список всех студентов с фильтром"""
    students = Student.objects.annotate(
        courses_count=Count('courses')
    )
    
    # Фильтр по наличию курсов
    no_courses = request.GET.get('no_courses')
    if no_courses:
        students = students.filter(courses_count=0)
    
    return render(request, 'schedule/student_list.html', {
        'students': students,
        'no_courses': no_courses
    })


def student_detail(request, student_id):
    """Детальная страница студента"""
    student = get_object_or_404(Student, id=student_id)
    available_courses = Course.objects.exclude(id__in=student.courses.all())
    return render(request, 'schedule/student_detail.html', {
        'student': student,
        'available_courses': available_courses
    })


def student_create(request):
    """Создание студента"""
    if request.method == 'POST':
        student = Student.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email']
        )
        messages.success(request, 'Студент создан!')
        return redirect('student_detail', student_id=student.id)
    
    return render(request, 'schedule/student_form.html')


def student_update(request, student_id):
    """Редактирование студента"""
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        student.first_name = request.POST['first_name']
        student.last_name = request.POST['last_name']
        student.email = request.POST['email']
        student.save()
        
        messages.success(request, 'Данные обновлены!')
        return redirect('student_detail', student_id=student.id)
    
    return render(request, 'schedule/student_form.html', {'student': student})


def student_delete(request, student_id):
    """Удаление студента"""
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Студент удален!')
        return redirect('student_list')
    
    return render(request, 'schedule/student_confirm_delete.html', {'student': student})


def student_enroll(request, student_id):
    """Запись студента на курс"""
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        course_id = request.POST['course_id']
        course = get_object_or_404(Course, id=course_id)
        student.courses.add(course)
        messages.success(request, f'Студент записан на курс "{course.title}"')
    
    return redirect('student_detail', student_id=student.id)


def student_drop(request, student_id, course_id):
    """Отписка студента от курса"""
    student = get_object_or_404(Student, id=student_id)
    course = get_object_or_404(Course, id=course_id)
    
    student.courses.remove(course)
    messages.success(request, f'Студент отписан от курса "{course.title}"')
    
    return redirect('student_detail', student_id=student.id)