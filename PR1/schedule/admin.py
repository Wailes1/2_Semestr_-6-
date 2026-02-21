from django.contrib import admin
from .models import Teacher, TeacherInfo, Course, Student

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'email', 'specialization']
    search_fields = ['last_name', 'first_name', 'email']

@admin.register(TeacherInfo)
class TeacherInfoAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'education', 'office_number']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'teacher', 'price']
    list_filter = ['teacher']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'email']
    filter_horizontal = ['courses']