from django.shortcuts import render
from .forms import TaskForm


def home(request):
    task_form = TaskForm(request.POST or None)

    return render(request, 'reminder/home.html', {
        'task_form': task_form,
    })
