import requests
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist, ValidationError  
from django.views import generic
# Rest Framework imports
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.views import JSONWebTokenAPIView
from rest_framework import viewsets
# local imports
from manufacturer.models import Manufacturer
from manufacturer.api.serializers import ( ManufacturerSerializer, 
                                     
                                )
#from Manufacturer.utils import generate_jwt_token
#from Manufacturer.tasks import add


class ManufacturerViewSet(generics.ListAPIView):

    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer

class ManufacturerSearchView(generics.ListAPIView):
    serializer_class = ManufacturerSerializer
    queryset = Manufacturer.objects.all()	

    def get_queryset(self):
        qs = Manufacturer.objects.all()
        query = self.request.GET.get('q')
        if query is not None:
            data = qs.filter(Q(name__icontains=query))
        else:
            data = {}
        return data


class AddNewManufacturer(generics.ListCreateAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer


class UpdateManufacturer(generics.RetrieveUpdateAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    lookup_field = 'id'

class ManufacturerDeleteView(generics.DestroyAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    lookup_field = 'id'
