from django.conf.urls import url
from .views import home, category_details, delete_expense, edit_expense, create_category_view, delete_category


urlpatterns = [
    url(r'^home/$', home, name='home'),
    url(r'^category/new/$', create_category_view, name='create-category'),
    url(r'^category/(?P<slug>[-\w]+)/$', category_details, name='category-details'),
    url(r'^edit-expense/(?P<pk>\d+)/$', edit_expense, name='edit-expense'),
    url(r'^delete-expense/(?P<pk>\d+)/$', delete_expense, name='delete-expense'),
    url(r'^delete-category/(?P<pk>\d+)/$', delete_category, name='delete-category')

]
