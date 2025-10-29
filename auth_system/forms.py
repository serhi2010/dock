from django import forms
from django.contrib.auth.forms import UserCreationForm
from auth_system.models import CustomUser

class StudentRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'student'
        if commit:
            user.save()
        return user

class RoleUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['role']
        labels = {'role': 'Нова роль'}