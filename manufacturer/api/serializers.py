from __future__ import unicode_literals


import logging
import datetime
import calendar

from django.db import transaction 

from rest_framework import serializers

from manufacturer.models import Manufacturer

class ManufacturerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Manufacturer
        fields = '__all__'

    def create(self, validated_data):
        return Manufacturer.objects.create(**validated_data)



