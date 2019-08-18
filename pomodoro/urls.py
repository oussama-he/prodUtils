from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'home/', views.home, name='home'),
    url(r'start/', views.start, name='start'),
    url(r'finish/', views.finish, name='finish'),
    url(r'new-task/', views.new_task, name='new'),
    url(r'project/new/', views.add_project, name='new-project'),
    url(r'project/(?P<pk>\d+)/delete/', views.delete_project, name='project-delete'),
    url(r'project/(?P<pk>\d+)/detail/', views.project_detail, name='project-detail'),
    url(r'task/(?P<pk>\d+)/detail/$', views.task_detail, name='task-detail'),
    url(r'task/(?P<pk>\d+)/delete/$', views.delete_task, name='task-delete'),
    url(r'^history/$', views.session, name='history'),
    url(r'history/(?P<pk>\d+)/delete/', views.delete_history, name='history-delete'),
    url(r'generate-pdf/', views.generate_pdf, name='generate-pdf'),
    url(r'projects/', views.get_all_projects, name='projects'),
    url(r'^task/(?P<pk>\d+)$', views.get_tasks, name='tasks'),

]
