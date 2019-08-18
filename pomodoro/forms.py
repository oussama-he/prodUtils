from django import forms
from .models import Task, Project


class NewTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['project', 'title',]


class NewProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', ]
