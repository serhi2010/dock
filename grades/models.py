from django.db import models
from django.conf import settings
from courses.models import Lesson
from courses.models import Course
from auth_system.models import CustomUser

class Grade(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='grades')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='grades')
    score = models.PositiveIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'lesson')

    def __str__(self):
        return f"{self.student} → {self.lesson}: {self.score}"

class CourseEnrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='course_enrollments')

