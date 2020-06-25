from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
    date_of_birth = models.DateField(default="1970-01-01")
    phone_number = models.CharField(max_length=15, default='')
    fullname = models.TextField(default='')



class PasswordCode(models.Model):
	email = models.EmailField()
	code = models.CharField(max_length=100)