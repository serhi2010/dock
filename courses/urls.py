from django.urls import path
from . import views

app_name = 'courses'  # Це дозволяє використовувати namespace 'courses' у шаблонах

urlpatterns = [
    # 📚 Курси
    path('', views.course_list, name='course_list'),
    path('create/', views.course_create, name='course_create'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('<int:course_id>/edit/', views.course_edit, name='course_edit'),
    path('<int:course_id>/enroll/', views.enroll_course, name='enroll'),


    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student/', views.student_dashboard, name='student_dashboard'),


    path('<int:course_id>/add-module/', views.add_module, name='add_module'),
    path('module/<int:module_id>/', views.module_detail, name='module_detail'),
    path('module/<int:module_id>/add-lesson/', views.add_lesson, name='add_lesson'),
    path('<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    path('<int:course_id>/unenroll/', views.unenroll_course, name='unenroll_course'),



    path('lessons/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('lessons/', views.lesson_list, name='lesson_list'),
]
