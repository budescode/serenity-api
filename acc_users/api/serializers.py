from rest_framework import serializers
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.Serializer):
    fullname = serializers.CharField(max_length=250)
    email = serializers.EmailField(max_length=250)
    phone_number = serializers.CharField(max_length=250)
    password = serializers.CharField(max_length=250)

class CheckPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=250)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = []

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200)

class ValidateEmailSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=200)
    code = serializers.CharField(max_length=200)

class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=200)
    email = serializers.CharField(max_length=200)
    code = serializers.CharField(max_length=200)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=200)
    new_password = serializers.CharField(max_length=200)

class EditProfileSerializer(serializers.Serializer):
    email = serializers.EmailField()
    fullname = serializers.CharField(max_length=50)
    phone_number = serializers.CharField(max_length=50)
    occupation = serializers.CharField(max_length=50)
    home_address = serializers.CharField(max_length=50)
    state = serializers.CharField(max_length=50)
    city = serializers.CharField(max_length=50)
    marital_status = serializers.CharField(max_length=50)
    educational_level = serializers.CharField(max_length=50)
    # fullname = serializers.CharField(max_length=50)
    # fullname = serializers.CharField(max_length=50)
    # fullname = serializers.CharField(max_length=50)
    # class Meta:
    #     model = get_user_model()
        #fields = ['email', 'fullname', 'phone_number', 'occupation', 'home_address', 'state', 'city', 'marital_status', 'educational_level']