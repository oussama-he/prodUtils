from django.conf.urls import url
from .views import home, create, archive, delete

urlpatterns = [
    url(r'^home/$', home, name='home'),
    url(r'^create/$', create, name='create'),
    url(r'^(?P<pk>\d+)/archive/$', archive, name='archive'),
    url(r'^(?P<pk>\d+)/delete/$', delete, name='delete'),
    ]
