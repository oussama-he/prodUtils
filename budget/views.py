from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .models import Expense, Category
from .forms import ExpenseForm, EditExpenseForm, CategoryForm


def home(request):
    categories = Category.objects.all()
    total_expenses = 0
    category_form = CategoryForm()
    for category in categories:
        total_expenses += category.get_total_cost()

    form = ExpenseForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            expense = form.save(commit=False)
            expense.save()
            return redirect("budget:home")
    else:
        form = ExpenseForm()
    return render(request, 'budget/home.html', {
        'form': form,
        'total_expenses': total_expenses,
        'categories': categories,
        'category_form': category_form
    })


def create_category_view(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            return JsonResponse({"status": "ok"}, safe=False, status=201)
        else:
            errors = form.errors.as_json()
            return JsonResponse(errors, safe=False, status=500)
    # return redirect('budget:home')


def category_details(request, slug):
    return render(request, 'budget/category-details.html', {
        'category': Category.objects.get(slug=slug)
    })


def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    
    if request.method == 'POST':
        form = EditExpenseForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return HttpResponseRedirect(expense.category.get_absolute_url())
    else:
        form = EditExpenseForm(instance=expense)
    
    return render(request, 'budget/edit-expense.html', {
        'form': form,
        'expense': expense
    })

def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)

    if request.method == 'POST':
        expense.delete()
        return redirect('budget:category-details', slug=expense.category.slug)
    
    return render(request, 'budget/delete-object.html', {
        'object': expense
    })