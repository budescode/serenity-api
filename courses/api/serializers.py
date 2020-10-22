from rest_framework import serializers
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
from courses.models import Beginners, Intermediate, Advance


class BeginnersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beginners()
        exclude = []

class IntermediateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intermediate()
        exclude = []

class AdvanceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advance()
        exclude = []
