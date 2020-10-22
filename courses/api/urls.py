from django.urls import path, include
from django.conf.urls import url
from . import views


app_name = 'courses_api'
#from index.api.views import SchoolCreateView, AddressCreateView, StudentCreateView, SubjectCreateView ,SchoolListView, AddressListView, StudentListView, SubjectListView


urlpatterns = [
path('beginnnerlist/', views.BeginnersListView, name='beginnerlist'),

]