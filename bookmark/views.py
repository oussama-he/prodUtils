from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from bookmark.models import Bookmark, Category
from .forms import BookmarkForm, CategoryForm


def home(request):
    categories = Category.objects.all()

    return render(request, 'bookmark/home.html', {
        'categories': categories,
    })


def create(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = BookmarkForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            instance = form.save(commit=False)
            instance.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('bookmark:home'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = BookmarkForm()
    return render(request, 'bookmark/create.html', {
        'form': form,
        'title': 'Create New Bookmark'
    })


def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return HttpResponseRedirect(reverse('bookmark:home'))
    else:
        form = CategoryForm()
    return render(request, 'bookmark/create.html', {
        'form': form,
        'title': 'Create New Category'
    })


def archive(request, pk):
    bookmark = get_object_or_404(Bookmark, pk=pk)
    if request.method == 'POST':
        bookmark.archive = True
        bookmark.save()
        return redirect('bookmark:home')

    return render(request, 'bookmark/archive.html', {'bookmark': bookmark})
