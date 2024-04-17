from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MaxLengthValidator

User._meta.get_field('username').validators.append(MaxLengthValidator(limit_value=20))

class List(models.Model):
    title = models.CharField(max_length=50, verbose_name='Список')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='participants')
    is_completed = models.BooleanField(default=False, verbose_name='Выполнено')
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tasks', kwargs={'list_id': self.id})
    
    class Meta:
        ordering = ['is_completed', '-time_create']

    def is_list_completed(self):
        total_tasks = self.tasks.count()
        completed_tasks = self.tasks.filter(is_completed=True).count()
        return total_tasks > 0 and total_tasks == completed_tasks

    
class Task(models.Model):
    title = models.CharField(max_length=50, verbose_name='Задача')
    list = models.ForeignKey('List', on_delete=models.CASCADE, related_name='tasks', verbose_name='Список')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_completed = models.BooleanField(default=False, verbose_name='Выполнено')

    class Meta:
        ordering = ['is_completed', '-time_create']

    def __str__(self):
        return self.title
    
class Invitation(models.Model):

    class Status(models.TextChoices):
        WAITING = 'Waiting'
        ACCEPTED = 'Accepted'
        REJECTED = 'Rejected'

    user_from = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invitations_from')
    user_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invitations_to')
    list = models.ForeignKey('List', on_delete=models.CASCADE, related_name='invitation')
    time_create = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.WAITING)

    class Meta:
        ordering = ['time_create']

    def __str__(self):
        return f'from {self.user_from.username} to {self.user_to.username}'
