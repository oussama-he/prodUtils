from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(('pomodoro.urls', 'pomodoro'), namespace='pomodoro')),
]
