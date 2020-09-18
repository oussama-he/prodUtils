from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'home/', views.home, name='home'),
    url(r'start/', views.start, name='start'),
    url(r'finish/', views.finish, name='finish'),
    url(r'new-task/', views.new_task, name='new'),
    url(r'^tasks/$', views.all_tasks, name='all-tasks'),
    url(r'project/new/', views.add_project, name='new-project'),
    url(r'projects/', views.get_all_projects, name='projects'),
    url(r'^project/(?P<pk>\d+)$', views.get_project_tasks, name='project-tasks'),
    url(r'project/(?P<pk>\d+)/delete/', views.delete_project, name='project-delete'),
    url(r'project/(?P<pk>\d+)/detail/', views.project_detail, name='project-detail'),
    url(r'task/(?P<pk>\d+)/detail/$', views.task_detail, name='task-detail'),
    url(r'^task/(?P<pk>\d+)/session/(?P<session_pk>\d+)/$', views.EditSessionView.as_view(), name='edit-session'),
    url(r'task/(?P<pk>\d+)/delete/$', views.delete_task, name='task-delete'),
    url(r'^task/(?P<pk>\d+)/edit', views.EditTaskView.as_view(), name='task-edit'),
    url(r'history/(?P<pk>\d+)/delete/', views.delete_history, name='history-delete'),
    url(r'^stats/(?P<period>[\w-]+)', views.period_stats, name='period-stats'),
]
