from django.urls import path
from . import views

app_name = 'grades'


urlpatterns = [

    path('add/<int:lesson_id>/<int:student_id>/', views.add_grade, name='add_grade'),

    path('my/', views.student_grades, name='student_grades'),
    path('select/<int:course_id>/', views.select_student_for_grading, name='select_student'),
    path('dashboard/', views.grade_dashboard, name='grade_dashboard'),
    path('course/<int:course_id>/', views.grade_course_detail, name='grade_course_detail'),
    path('course/<int:course_id>/student/<int:student_id>/', views.grade_student, name='grade_student'),
]
