from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    title = forms.CharField(label='What to do?')
    time = forms.TimeField(label='At what time?')
    date = forms.DateField()

    class Meta:
        model = Task
        fields = ['title', 'time', 'date']