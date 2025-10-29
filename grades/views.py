from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Grade, CourseEnrollment
from .forms import GradeForm
from courses.models import Lesson, Course
from auth_system.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

# ✅ Додавання оцінки вручну
@login_required
def add_grade(request, lesson_id, student_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    student = get_object_or_404(User, pk=student_id)
    grade, _ = Grade.objects.get_or_create(student=student, lesson=lesson)

    if request.method == 'POST':
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            messages.success(request, 'Оцінка збережена.')
            return redirect('courses:lesson_detail', lesson_id=lesson.id)
    else:
        form = GradeForm(instance=grade)

    return render(request, 'grades/add_grade.html', {
        'form': form,
        'lesson': lesson,
        'student': student
    })

# ✅ Перегляд оцінок студентом
@login_required
def student_grades(request):
    grades = Grade.objects.filter(student=request.user).select_related('lesson')
    return render(request, 'grades/student_grades.html', {'grades': grades})

# ✅ Вибір учня для оцінювання
@login_required
def select_student_for_grading(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    students = course.students.all()
    return render(request, 'grades/select_student.html', {
        'course': course,
        'students': students
    })

# ✅ Панель викладача
@login_required
def grade_dashboard(request):
    if request.user.role != 'teacher':
        return redirect('courses:course_list')
    courses = Course.objects.filter(teacher=request.user)
    return render(request, 'grades/grade_dashboard.html', {'courses': courses})

# ✅ Таблиця оцінок по курсу (без templatetags)
@login_required
def grade_course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id, teacher=request.user)
    students = course.students.all()
    lessons = Lesson.objects.filter(module__course=course)
    grades = Grade.objects.filter(lesson__in=lessons, student__in=students)

    # Створюємо вкладений словник: grade_map[student_id][lesson_id] = grade
    grade_map = {}
    for student in students:
        grade_map[student.id] = {}
    for grade in grades:
        grade_map[grade.student_id][grade.lesson_id] = grade

    return render(request, 'grades/grade_course_detail.html', {
        'course': course,
        'students': students,
        'lessons': lessons,
        'grade_map': grade_map
    })

# ✅ Оцінювання конкретного учня
@login_required
def grade_student(request, course_id, student_id):
    course = get_object_or_404(Course, pk=course_id, teacher=request.user)
    student = get_object_or_404(CustomUser, pk=student_id, role='student')
    lessons = Lesson.objects.filter(module__course=course)

    selected_lesson_id = request.GET.get('lesson')
    selected_lesson = None
    grade = None

    if selected_lesson_id:
        selected_lesson = get_object_or_404(Lesson, pk=selected_lesson_id, module__course=course)
        try:
            grade = Grade.objects.get(student=student, lesson=selected_lesson)
        except Grade.DoesNotExist:
            grade = None

    if request.method == 'POST' and selected_lesson:
        form = GradeForm(request.POST, instance=grade) if grade else GradeForm(request.POST)
        if form.is_valid():
            new_grade = form.save(commit=False)
            new_grade.student = student
            new_grade.lesson = selected_lesson
            new_grade.save()
            messages.success(request, 'Оцінка збережена.')
            return redirect('grades:grade_course_detail', course_id=course.id)
    else:
        form = GradeForm(instance=grade) if selected_lesson else None

    return render(request, 'grades/grade_student.html', {
        'course': course,
        'student': student,
        'lessons': lessons,
        'selected_lesson': selected_lesson,
        'form': form
    })

# ✅ Запис на курс
@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.user.role != 'student':
        messages.error(request, 'Лише студенти можуть записуватись на курси.')
        return redirect('courses:course_detail', course_id=course.id)

    course.students.add(request.user)
    CourseEnrollment.objects.get_or_create(course=course, student=request.user)

    messages.success(request, f'Ви успішно записалися на курс "{course.title}"!')
    return redirect('courses:student_dashboard')

# ✅ Вихід з курсу
@login_required
def unenroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.user.role != 'student':
        messages.error(request, 'Лише студенти можуть виходити з курсів.')
        return redirect('courses:course_detail', course_id=course.id)

    course.students.remove(request.user)
    CourseEnrollment.objects.filter(course=course, student=request.user).delete()

    messages.success(request, f'Ви вийшли з курсу "{course.title}".')
    return redirect('courses:student_dashboard')
