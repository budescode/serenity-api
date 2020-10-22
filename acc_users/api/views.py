from rest_framework import generics
from acc_users.api.serializers import UserSerializer, LoginSerializer, PasswordResetSerializer, ValidateEmailSerializer, ChangePasswordSerializer, EditProfileSerializer, UserProfileSerializer, CheckPasswordSerializer
from acc_users.models import PasswordCode
from rest_framework import permissions
from django.db.models import Q
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework import status
from rest_framework.response import Response
from django.utils.decorators import method_decorator

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from django.contrib.auth import get_user_model, authenticate
from django.core.mail import send_mail
import random
import string
from random import choice
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

class UserLogin(generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = LoginSerializer
    # pagination_class = PostLimitOffsetPagination
    permission_classes = [
        permissions.AllowAny
    ]
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            theu = email.find('@')
            username = email[:theu]
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    user_token = Token.objects.get_or_create(user=user)
                    user_token = user_token[0]
                    user_token = user_token.key
                    userdetails = {}
                    userdetails['username'] = user.username
                    userdetails['email'] = user.email
                    userdetails['token'] = user_token
                    userdetails['phone_number'] = user.phone_number
                    userdetails['fullname'] = user.fullname
                    return Response(userdetails, status=status.HTTP_201_CREATED)
            else:
                data = {"message":"Invalid Login Details"}
                return Response(data, status=status.HTTP_404_NOT_FOUND)
        else:
            data = {"message":"input right fields"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
    def get_queryset(self):
        qs = []
        return qs

class CheckPassword(generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = CheckPasswordSerializer
    # pagination_class = PostLimitOffsetPagination
    permission_classes = [
        permissions.IsAuthenticated
    ]
    def post(self, request, format=None):
        serializer = CheckPasswordSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']
            user1 = get_user_model().objects.get(username = self.request.user.username)
            user = user1.check_password(password)
            if user:
                data = {'response':'correct password'}
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response('Invalid Password', status=status.HTTP_404_NOT_FOUND)
        else:
            return Response('Input right fields', status=status.HTTP_404_NOT_FOUND)
    def get_queryset(self):
        qs = []
        return qs

class UserProfile(generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = UserProfileSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]
    def get_queryset(self):
        qs = get_user_model().objects.filter(username = self.request.user.username)
        return qs


class UserRegister(generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = UserSerializer
    # pagination_class = PostLimitOffsetPagination
    permission_classes = [
        permissions.AllowAny
    ]
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            fullname = serializer.validated_data['fullname']
            phone_number = serializer.validated_data['phone_number']
            theu = email.find('@')
            username = email[:theu]
            if theu == '-1':
                data = {"message":"send a valid email"}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            try:
                user = get_user_model().objects.get(email=email, username=username)
                data = {"message":"Email already exist"}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            except:
                user = get_user_model().objects.create(
                username=username,
                fullname=fullname,
                email=email,
                phone_number=phone_number,
                )
                user.set_password(password)
                user.save()
                user_token = Token.objects.get_or_create(user=user)
                user_token = user_token[0]
                user_token = user_token.key
                data = {"fullname":fullname, "email":email, "phone_number":phone_number, "token":user_token}
                return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = {"message":"Input right fields"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    def get_queryset(self):
        qs = []
        return qs



class ResetPasswordView(generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = PasswordResetSerializer
    # pagination_class = PostLimitOffsetPagination
    permission_classes = [
        permissions.AllowAny
    ]
    def post(self, request, format=None):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']
            try:
                getcode = PasswordCode.objects.get(code=code, email=email)
                try:
                    user = get_user_model().objects.get(email=email)
                    user.set_password(password)
                    user.save()
                    getcode.delete()
                    return Response('password successfully changed', status=status.HTTP_201_CREATED)
                except get_user_model().DoesNotExist:
                    return Response('Invalid Email', status=status.HTTP_404_NOT_FOUND)
            except PasswordCode.DoesNotExist:
                return Response('Invalid code', status=status.HTTP_404_NOT_FOUND)

        else:
            return Response('Input right fields', status=status.HTTP_400_BAD_REQUEST)
    def get_queryset(self):
        qs = []
        return qs


class sendEmailValidation(generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = ValidateEmailSerializer
    # pagination_class = PostLimitOffsetPagination
    permission_classes = [
        permissions.AllowAny
    ]
    def post(self, request, format=None):
        serializer = ValidateEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']
            try:
                user = get_user_model().objects.get(email=email)
                subject = "Reset Password"
                from_email = settings.EMAIL_HOST_USER
                # Now we get the list of emails in a list form.
                to_email = [email]
                #Opening a file in python, with closes the file when its done running
                detail2 = code
                with open(settings.BASE_DIR + "/templates/account/change_password_email.txt") as sign_up_email_txt_file:
                    sign_up_message = sign_up_email_txt_file.read()
                message = EmailMultiAlternatives(subject=subject, body=sign_up_message,from_email=from_email, to=to_email )
                html_template = get_template("account/change_password_email.html").render({'detail2':detail2})
                message.attach_alternative(html_template, "text/html")
                message.send()
                createcode = PasswordCode.objects.create(email=email, code=code)
                return Response('email successfully sent', status=status.HTTP_200_OK)
            except get_user_model().DoesNotExist:
                return Response('Invalid Email', status=status.HTTP_404_NOT_FOUND)
        else:
            return Response('Input right fields', status=status.HTTP_400_BAD_REQUEST)
    def get_queryset(self):
        qs = []
        return qs


class ChangePasswordView(generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = ChangePasswordSerializer
    # pagination_class = PostLimitOffsetPagination
    permission_classes = [
        permissions.IsAuthenticated
    ]
    def post(self, request, format=None):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            user = get_user_model().objects.get(username=self.request.user.username)
            ch = user.check_password(old_password)
            if ch:
                user.set_password(new_password)
                user.save()
                return Response('successfully changed', status=status.HTTP_201_CREATED)
            else:
                return Response('Wrong Password', status=status.HTTP_404_NOT_FOUND)
        else:
            return Response('Input right fields', status=status.HTTP_400_BAD_REQUEST)
    def get_queryset(self):
        qs = []
        return qs


class EditProfileView(generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = EditProfileSerializer
    # pagination_class = PostLimitOffsetPagination
    permission_classes = [
        permissions.IsAuthenticated
    ]
    def post(self, request, format=None):
        serializer = EditProfileSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            fullname = serializer.validated_data['fullname']
            phone_number = serializer.validated_data['phone_number']
            occupation = serializer.validated_data['occupation']
            home_address = serializer.validated_data['home_address']
            state = serializer.validated_data['state']
            city = serializer.validated_data['city']
            marital_status = serializer.validated_data['marital_status']
            educational_level = serializer.validated_data['educational_level']
            myemail = self.request.user.email
            details = {"email":email, "fullname":fullname, "phone_number":phone_number, "occupation":occupation, "home_address":home_address, "state":state, "city":city, "marital_status":marital_status, "educational_level":educational_level}
            if not myemail == email:
                genemail = get_user_model().objects.filter(email=email)
                if genemail:
                    return Response('Email already exist', status=status.HTTP_400_BAD_REQUEST)
                else:
                    user = get_user_model().objects.get(username=self.request.user.username)
                    theu = email.find('@')
                    username = email[:theu]
                    user.email = email
                    user.username = username
                    user.fullname = fullname
                    user.phone_number = phone_number
                    user.occupation = occupation
                    user.home_address = home_address
                    user.state = state
                    user.city = city
                    user.marital_status = marital_status
                    user.educational_level = educational_level
                    user.save()
                    return Response(details, status=status.HTTP_201_CREATED)

            else:
                user = get_user_model().objects.get(username=self.request.user.username)
                theu = email.find('@')
                username = email[:theu]
                user.email = email
                user.username = username
                user.fullname = fullname
                user.phone_number = phone_number
                user.occupation = occupation
                user.home_address = home_address
                user.state = state
                user.city = city
                user.marital_status = marital_status
                user.educational_level = educational_level
                user.save()
                return Response(details, status=status.HTTP_201_CREATED)
        else:
            return Response('Input right fields', status=status.HTTP_400_BAD_REQUEST)
    def get_queryset(self):
        qs = []
        return qs
