from django.urls import path
from .views import (
    home, start, finish, all_tasks, get_all_projects, project_detail, task_detail, generate_period_report, period_stats,
    TaskCreate, TaskDelete, TaskEdit, ProjectCreate, ProjectDelete, ProjectEdit, SessionEdit, SessionDelete,
)


urlpatterns = [
    path('home/', home, name='home'),

    path('session/create/', start, name='session-create'),
    path('session/<int:pk>/edit/', SessionEdit.as_view(), name='session-edit'),
    path('session/<int:pk>/delete/', SessionDelete.as_view(), name='session-delete'),
    path('finish/', finish, name='session-finish'),

    path('task/', all_tasks, name='task-list'),
    path('task/create/', TaskCreate.as_view(), name='task-create'),
    path('task/<int:pk>/detail/', task_detail, name='task-detail'),
    path('task/<int:pk>/delete/', TaskDelete.as_view(), name='task-delete'),
    path('task/<int:pk>/edit/', TaskEdit.as_view(), name='task-edit'),

    path('project/', get_all_projects, name='project-list'),
    path('project/create/', ProjectCreate.as_view(), name='project-create'),
    path('project/<int:pk>/edit/', ProjectEdit.as_view(), name='project-edit'),
    path('project/<int:pk>/delete/', ProjectDelete.as_view(), name='project-delete'),
    path('project/<int:pk>/detail/', project_detail, name='project-detail'),

    path('stats/<str:period>/', period_stats, name='period-stats'),
    path('report/<str:period>/', generate_period_report, name='period-report'),
]
