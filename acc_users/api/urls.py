from django.urls import path, include
from django.conf.urls import url
from . import views


app_name = 'account_api'
#from index.api.views import SchoolCreateView, AddressCreateView, StudentCreateView, SubjectCreateView ,SchoolListView, AddressListView, StudentListView, SubjectListView


urlpatterns = [
path('usercreate/', views.UserRegister.as_view(), name='usercreate'),
path('rest-auth/facebook/', views.FacebookLogin.as_view(), name='fb_login'),
path('login/', views.UserLogin.as_view(), name='login'),
path('resetpassword/', views.ResetPasswordView.as_view(), name='passwordchange'),
path('sendmailvalidation/', views.sendEmailValidation.as_view(), name='sendmail'),
path('changeuserpassword/', views.ChangePasswordView.as_view(), name='changeuserpassword'),
path('edituser/', views.EditProfileView.as_view(), name='edituser'),
path('userprofile/', views.UserProfile.as_view(), name='userprofile'),
path('checkpassword/', views.CheckPassword.as_view(), name='checkpassword'),
# path('detail/', views.DetailView.as_view(), name='detailview'),
]