from django.contrib import admin
from .models import Bookmark, Category


admin.site.register(Bookmark)
admin.site.register(Category)