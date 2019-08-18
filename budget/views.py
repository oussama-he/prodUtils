from django.shortcuts import render, redirect

from budget.forms import ExpenseForm
from .models import Expense, Category


def home(request):
    expenses = Expense.objects.all()
    categories = Category.objects.all()
    total_expenses = 0
    for expense in expenses:
        total_expenses += expense.cost

    form = ExpenseForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            expense = form.save(commit=False)
            expense.save()
            return redirect("budget:home")
    else:
        form = ExpenseForm()
    return render(request, 'budget/home.html', {
        'expenses': expenses,
        'form': form,
        'total_expenses': total_expenses,
        'categories': categories,
    })


