#!/usr/bin/env python

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Python imports.
import logging
import datetime
import calendar

# Django imports.
from django.db import transaction 

# Rest Framework imports.
from rest_framework import serializers

# Third Party Library imports

# local imports.
from users.models import *
from phonenumber_field.serializerfields import PhoneNumberField




class UserCreateSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()    
    password = serializers.CharField(write_only=True)

    def validate(self, data, *args, **kwargs):
       return super(UserCreateSerializer, self).validate(data, *args, **kwargs)


    def create(self, validated_data):
        phone_number = validated_data.get('phone_number')
        name = validated_data.get('name')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        user_type = validated_data.get('user_type')
        email = validated_data.get('email')
        user_type = validated_data.get('user_type', 'foodie')
        is_action = False
        is_phone_number_verified = False
        is_email_verified = False
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('phone_number', 'email', 'password', 'name', 'first_name', 'last_name', 'user_type')


class UserListSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()    

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'user_type', 'phone_number')


class UserSignupSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()    
    
    class Meta:
        model = User
        fields = ('phone_number', 'email', 'password')
    
    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data.get('email'),
            phone_number=validated_data['phone_number'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
   
    phone_number = serializers.IntegerField()
    password = serializers.CharField(write_only=True)
    @property
    def object(self):
        return self.validated_data
    def validate(self, attrs, *args, **kwargs):
        credentials = attrs
        if all(credentials.values()):
            user = self.authenticate(credentials['phone_number'],credentials['password'])            
            if user:
                if not user.is_active:
                    msg = 'User account is disabled.'
                else:    
                    return {'user': user}
            msg = 'Unable to login with provided credentials.'
            
        else:
            msg = 'Unable to login with provided credentials.'
        raise serializers.ValidationError(msg)
    def authenticate(self,phone_number=None, password=None):
        try:
            user = User.objects.get(phone_number=phone_number)
            check_pwd = user.check_password(password)
            if user and check_pwd:
                return user
            else:
                return None
        except:
            return None


class RefreshTokenSerializer(serializers.Serializer):
    
    existing_token = serializers.CharField(max_length=None, min_length=None, allow_blank=False, trim_whitespace=True)
    phone_number = serializers.IntegerField(max_value=None, min_value=None)
    password = serializers.CharField(max_length=None, min_length=None, allow_blank=False, trim_whitespace=True)


# class UserUpdateSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = UserProfile
#         fields = '__all__'

class OtpSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()    


class VerifyOtpSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()    
    otp = serializers.IntegerField()    
