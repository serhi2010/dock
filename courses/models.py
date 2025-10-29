from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

# 🧑‍🏫 Курс
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses'
    )
    students = models.ManyToManyField(User, related_name='enrolled_courses', blank=True)

    def __str__(self):
        return self.title

    def get_lessons(self):
        return Lesson.objects.filter(module__course=self)

    def student_count(self):
        return self.students.count()

    def get_teacher_name(self):
        return f"{self.teacher.first_name} {self.teacher.last_name}"

    def short_description(self):
        return self.description[:100] + "..." if len(self.description) > 100 else self.description


# 📦 Модуль курсу
class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} — {self.title}"

    def lesson_count(self):
        return self.lessons.count()


# 📘 Урок
class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='lesson_images/', blank=True, null=True)
    video_url = models.URLField(blank=True)
    assignment = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.module.title} — {self.title}"