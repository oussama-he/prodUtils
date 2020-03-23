from django import forms
from .models import Task, Project, Session


class NewTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['project', 'title',]


class EditTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['project', 'title']


class EditSessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['task', 'start_time', 'finish_time', 'interrupted']


class NewProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', ]
