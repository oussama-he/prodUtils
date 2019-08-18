from django import forms
from .models import Bookmark, Category


class BookmarkForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), required=False)

    class Meta:
        model = Bookmark
        fields = ['title', 'link', 'category', 'description', 'safe']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', ]