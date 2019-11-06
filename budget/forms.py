from django import forms
from .models import Expense, Category
from django.utils import timezone


class ExpenseForm(forms.ModelForm):
    timestamp = forms.DateField(initial=timezone.now(), required=False)

    class Meta:
        model = Expense
        fields = ['cost', 'timestamp', 'category','notes', ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4, }),
        }


class EditExpenseForm(forms.ModelForm):

    class Meta:
        model = Expense
        exclude = ['added_at']


class CategoryForm(forms.ModelForm):
    
    class Meta:
        model = Category
        exclude = ['slug']