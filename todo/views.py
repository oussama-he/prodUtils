from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from todo.forms import ToDoForm
from .models import Set, ToDo


def home(request):
    sets = Set.objects.all()
    return render(request, 'todo/home.html', {'sets': sets})


def create(request):
    if request.method == 'POST':
        form = ToDoForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return HttpResponseRedirect(reverse("todo:home"))
    else:
        form = ToDoForm()
    return render(request, 'todo/create.html', {
        'form': form,
        'title': "create new ToDo"
    })


def archive(request, pk):
    todo = get_object_or_404(ToDo, pk=pk)
    todo.done = True
    todo.save()
    return redirect('todo:home')


def delete(request, pk):
    todo = get_object_or_404(ToDo, pk=pk)
    if request.method == 'POST':
        todo.delete()
        return redirect('todo:home')
    return render(request, 'todo/confirm_delete.html', {'object': todo})


