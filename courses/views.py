from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model

from .models import Course, Module, Lesson
from .forms import CourseForm, ModuleForm
from .forms import LessonForm
from .models import Lesson
User = get_user_model()

# 📋 Список курсів
def course_list(request):
    courses = Course.objects.all()
    teacher_id = request.GET.get('teacher')
    search_query = request.GET.get('q')

    if teacher_id:
        courses = courses.filter(teacher_id=teacher_id)
    if search_query:
        courses = courses.filter(title__icontains=search_query)

    teachers = User.objects.filter(role='teacher')
    return render(request, 'courses/course_list.html', {
        'courses': courses,
        'teachers': teachers,
        'search_query': search_query,
        'selected_teacher': teacher_id
    })

# 📘 Деталі курсу + модулі
@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    modules = course.modules.all().order_by('order')
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'modules': modules
    })

# 🆕 Створення курсу
@login_required
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
            messages.success(request, 'Курс успішно створено.')
            return redirect('courses:teacher_dashboard')
    else:
        form = CourseForm()
    return render(request, 'courses/create_course.html', {'form': form})

# 🧑‍🏫 Панель вчителя
@login_required
def teacher_dashboard(request):
    if request.user.role != 'teacher':
        return redirect('courses:course_list')
    courses = Course.objects.filter(teacher=request.user)
    return render(request, 'courses/teacher_dashboard.html', {'courses': courses})

# 🧑‍🎓 Панель учня
@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        return redirect('courses:course_list')
    enrolled_courses = request.user.enrolled_courses.all()
    return render(request, 'courses/student_dashboard.html', {'courses': enrolled_courses})

# ✏️ Редагування курсу
@login_required
def course_edit(request, course_id):
    course = get_object_or_404(Course, id=course_id, teacher=request.user)
    form = CourseForm(request.POST or None, instance=course)
    form.set_user(request.user)  # якщо форма має метод set_user

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Курс оновлено.')
            return redirect('courses:course_detail', course_id=course.id)

    return render(request, 'courses/course_edit.html', {'form': form, 'course': course})

# ✅ Запис на курс
@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.user.role != 'student':
        messages.error(request, 'Лише студенти можуть записуватись на курси.')
        return redirect('courses:course_detail', course_id=course.id)

    course.students.add(request.user)
    messages.success(request, f'Ви успішно записалися на курс "{course.title}"!')
    return redirect('courses:student_dashboard')

@login_required
def add_module(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.user != course.teacher:
        messages.error(request, 'Лише автор курсу може додавати модулі.')
        return redirect('courses:course_detail', course_id=course.id)

    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            module = form.save(commit=False)
            module.course = course
            module.save()
            messages.success(request, f'Модуль "{module.title}" успішно додано.')
            return redirect('courses:course_detail', course_id=course.id)
    else:
        form = ModuleForm()

    return render(request, 'courses/add_module.html', {'form': form, 'course': course})

@login_required
def add_lesson(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    course = module.course

    if request.user != course.teacher:
        messages.error(request, 'Лише автор курсу може додавати уроки.')
        return redirect('courses:course_detail', course_id=course.id)

    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.module = module
            lesson.save()
            messages.success(request, f'Урок "{lesson.title}" додано.')
            return redirect('courses:course_detail', course_id=course.id)
    else:
        form = LessonForm()

    return render(request, 'courses/add_lesson.html', {'form': form, 'module': module})

@login_required
def module_detail(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    course = module.course

    # 🔐 Доступ лише для учнів, вчителів, адміністраторів
    if request.user.role not in ['student', 'teacher', 'admin']:
        return HttpResponseForbidden("⛔ У вас немає доступу до цього модуля.")

    # 🔍 Якщо це учень — перевір, чи він записаний на курс
    if request.user.role == 'student':
        if request.user not in course.students.all():
            messages.error(request, '⛔ Ви не записані на цей курс.')
            return redirect('courses:course_list')

    return render(request, 'courses/module_detail.html', {'module': module})


def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    return render(request, 'lessons/lesson_detail.html', {'lesson': lesson})


def lesson_list(request):
    lessons = Lesson.objects.all()
    return render(request, 'courses/lesson_list.html', {'lessons': lessons})


@login_required
def unenroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.user.role != 'student':
        messages.error(request, 'Лише студенти можуть виходити з курсів.')
        return redirect('courses:course_detail', course_id=course.id)

    course.students.remove(request.user)
    messages.success(request, f'Ви вийшли з курсу "{course.title}".')
    return redirect('courses:student_dashboard')
