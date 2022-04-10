from __future__ import unicode_literals


import logging
import datetime
import calendar

from django.db import transaction 

from rest_framework import serializers

from invoice.models import Invoice, InvoiceItem


class InvoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invoice
        fields = '__all__'

    def create(self, validated_data):
        return Invoice.objects.create(**validated_data)


class InvoiceItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvoiceItem
        fields = '__all__'

    def create(self, validated_data):
        return InvoiceItem.objects.create(**validated_data)




