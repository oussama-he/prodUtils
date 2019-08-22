from django import forms
from .models import Expense
from django.utils import timezone


class ExpenseForm(forms.ModelForm):
    timestamp = forms.DateField(initial=timezone.now())

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