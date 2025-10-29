from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from auth_system.models import CustomUser

# 🔧 Додаткова дія для масової зміни ролі
@admin.action(description='Змінити роль на Вчитель')
def make_teacher(modeladmin, request, queryset):
    queryset.update(role='teacher')

@admin.action(description='Змінити роль на Учень')
def make_student(modeladmin, request, queryset):
    queryset.update(role='student')

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'is_staff', 'is_superuser']
    list_filter = ['role', 'is_staff', 'is_superuser']
    search_fields = ['username', 'email']
    ordering = ['username']
    actions = [make_teacher, make_student]  # ✅ Масові дії

    # 🔧 Додаємо поле role до форми редагування
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )

    # 🔧 Додаємо поле role до форми створення
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
