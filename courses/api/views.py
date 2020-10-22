from rest_framework import generics
from courses.api.serializers import BeginnersListSerializer, IntermediateListSerializer, AdvanceListSerializer
from courses.models import Beginners, Intermediate, Advance
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
from rest_framework.decorators import api_view, permission_classes

from django.contrib.auth import get_user_model, authenticate
from rest_framework.pagination import PageNumberPagination
from .pagination import StandardResultsSetPagination, PostLimitOffsetPagination

# class BeginnersListView(generics.ListAPIView):
# 	lookup_field = 'pk'
# 	serializer_class = BeginnersListSerializer
# 	pagination_class = StandardResultsSetPagination
# 	permission_classes = [
# 	    permissions.AllowAny
# 	]
# 	def get_queryset(self):
# 	    qs = Beginners.objects.all().filter(active=True)
# 	    data = {'details':qs}
# 	    return qs


@api_view(['GET'])
@permission_classes([permissions.AllowAny]) #this is to get a specific user all courses
def BeginnersListView(request):
    beginner = Beginners.objects.filter(active=True)
    beginnerlist = BeginnersListSerializer(beginner, many=True).data
    intermediate = Intermediate.objects.filter(active=True)
    intermediatelist = IntermediateListSerializer(intermediate, many=True).data
    advanced = Advance.objects.filter(active=True)
    advancedlist = AdvanceListSerializer(advanced, many=True).data
    data = {"detail":"success", 'beginner':beginnerlist, 'intermediate':intermediatelist, 'advanced':advancedlist}
    return Response(data, status=status.HTTP_200_OK)