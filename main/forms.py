from django import forms
from django.contrib.auth.models import User

from .models import Task, List

class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title']

class AddListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ['title']

# class InviteUserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username']

class InviteUserForm(forms.Form):
    username = forms.CharField(max_length=150)
