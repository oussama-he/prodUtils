from django.conf.urls import url
from .views import create, home, create_category, archive

urlpatterns = [
    url(r'^create/$', create, name='create'),
    url(r'^category/create$', create_category, name='create-category'),
    url(r'^home/$', home, name='home'),
    url(r'^(?P<pk>\d+)/archive/$', archive, name='archive'),
]
