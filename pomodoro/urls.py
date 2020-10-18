from django.conf.urls import url
from .views import (
    home, start, finish, all_tasks, get_all_projects, get_project_tasks, project_detail, task_detail,
    TaskCreate, TaskDelete, TaskEdit, ProjectCreate, ProjectDelete, ProjectEdit, SessionEdit, SessionDelete,
    generate_period_report, period_stats,
)


urlpatterns = [
    url(r'home/', home, name='home'),
    url(r'start/', start, name='start'),
    url(r'finish/', finish, name='finish'),
    url(r'new-task/', TaskCreate.as_view(), name='new'),
    url(r'^tasks/$', all_tasks, name='all-tasks'),
    url(r'project/new/', ProjectCreate.as_view(), name='new-project'),
    url(r'projects/', get_all_projects, name='projects'),
    url(r'^project/(?P<pk>\d+)$', get_project_tasks, name='project-tasks'),
    url(r'project/(?P<pk>\d+)/delete/', ProjectDelete.as_view(), name='project-delete'),
    url(r'project/(?P<pk>\d+)/detail/', project_detail, name='project-detail'),
    url(r'^project/(?P<pk>\d+)/edit/$', ProjectEdit.as_view(), name='project-edit'),
    url(r'task/(?P<pk>\d+)/detail/$', task_detail, name='task-detail'),
    url(r'^task/(?P<pk>\d+)/session/(?P<session_pk>\d+)/$', SessionEdit.as_view(), name='edit-session'),
    url(r'task/(?P<pk>\d+)/delete/$', TaskDelete.as_view(), name='task-delete'),
    url(r'^task/(?P<pk>\d+)/edit', TaskEdit.as_view(), name='task-edit'),
    url(r'session/(?P<pk>\d+)/delete/', SessionDelete.as_view(), name='history-delete'),
    url(r'^stats/(?P<period>[\w-]+)', period_stats, name='period-stats'),
    url(r'^report/(?P<period>[\w-]+)', generate_period_report, name='period-report'),
]
