from django import forms
from .models import Grade

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['score', 'comment']
        widgets = {
            'score': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введіть оцінку',
                'min': 1,
                'max': 12
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Коментар (необов’язково)',
                'rows': 2
            })
        }
        labels = {
            'score': 'Оцінка',
            'comment': 'Коментар'
        }
