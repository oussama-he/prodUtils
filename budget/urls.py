from django.conf.urls import url
from .views import home, category_details, delete_expense, edit_expense

urlpatterns = [
    url(r'^home/$', home, name='home'),
    url(r'^category/(?P<slug>[-\w]+)/$', category_details, name='category-details'),
    url(r'^edit-expense/(?P<pk>\d+)/$', edit_expense, name='edit-expense'),
    url(r'^delete-expense/(?P<pk>\d+)/$', delete_expense, name='delete-expense'),

]
