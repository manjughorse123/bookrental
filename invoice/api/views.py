import requests

# Django imports
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
from invoice.models import Invoice, InvoiceItem
from invoice.api.serializers import ( InvoiceSerializer, 
                                     InvoiceItemSerializer,
                                )

class InvoiceViewSet(generics.ListAPIView):

    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

class InvoiceItemViewSet(generics.ListAPIView):

    queryset = InvoiceItem.objects.all()
    serializer_class = InvoiceItemSerializer


class InvoiceSearchView(generics.ListAPIView):
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()	

    def get_queryset(self):
        qs = Invoice.objects.all()
        query = self.request.GET.get('q')
        if query is not None:
            data = qs.filter(Q(name__icontains=query))
        else:
            data = {}
        return data


class AddNewInvoice(generics.ListCreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


class UpdateInvoice(generics.RetrieveUpdateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    lookup_field = 'id'

class InvoiceDeleteView(generics.DestroyAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    lookup_field = 'id'
