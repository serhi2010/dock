from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.auth import get_user_model
from .models import CustomUser
from .forms import RoleUpdateForm

from .forms import StudentRegistrationForm
User = get_user_model()

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

def register(request):
    if request.user.is_authenticated:
        if request.user.role == 'teacher':
            return redirect('courses:teacher_dashboard')
        elif request.user.role == 'admin':
            return redirect('admin_panel')
        else:
            return redirect('courses:student_dashboard')

    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Реєстрація успішна!')

            if user.role == 'teacher':
                return redirect('courses:teacher_dashboard')
            elif user.role == 'admin':
                return redirect('admin_panel')
            else:
                return redirect('courses:student_dashboard')
        else:
            messages.error(request, 'Помилка у формі.')
    else:
        form = StudentRegistrationForm()

    return render(request, 'auth_system/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        if request.user.role == 'teacher':
            return redirect('courses:teacher_dashboard')
        elif request.user.role == 'admin':
            return redirect('admin_panel')
        else:
            return redirect('courses:student_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Вхід успішний!')
            if user.role == 'teacher':
                return redirect('courses:teacher_dashboard')
            elif user.role == 'admin':
                return redirect('admin_panel')
            else:
                return redirect('courses:student_dashboard')
        else:
            messages.error(request, 'Невірні дані.')

    return render(request, 'auth_system/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Ви вийшли з системи.')
    return redirect('login')

@user_passes_test(lambda u: u.is_superuser)
def admin_panel(request):
    users = User.objects.all()
    return render(request, 'auth_system/admin_panel.html', {'users': users})

@login_required
def delete_user(request, user_id):
    if not request.user.role == 'admin' and not request.user.is_superuser:
        return HttpResponseForbidden('⛔ Лише адміністратори можуть видаляти акаунти')

    user_to_delete = get_object_or_404(User, pk=user_id)
    if user_to_delete == request.user:
        messages.error(request, '⛔ Ви не можете видалити свій акаунт')
        return redirect('admin_panel')

    user_to_delete.delete()
    messages.success(request, f'✅ Користувача {user_to_delete.username} видалено')
    return redirect('admin_panel')

@login_required
@user_passes_test(lambda u: u.role == 'admin')
def update_user_role(request, user_id):
    user_to_update = get_object_or_404(CustomUser, pk=user_id)

    if request.method == 'POST':
        form = RoleUpdateForm(request.POST, instance=user_to_update)
        if form.is_valid():
            form.save()
            messages.success(request, f'✅ Роль користувача {user_to_update.username} оновлено')
            return redirect('admin_panel')
    else:
        form = RoleUpdateForm(instance=user_to_update)

    return render(request, 'auth_system/update_role.html', {'form': form, 'user': user_to_update})