# Python Imports
import re
import os
import sys
import time
import base64
import copy
import json
import datetime
from django.contrib.auth import logout
import requests
import random


# Django imports
from django.http import HttpResponse
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist, ValidationError  
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
# Rest Framework imports
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from users.serializers_jwt import JSONWebTokenSerializer
from rest_framework_jwt.views import JSONWebTokenAPIView
from rest_framework import generics
#from users.utils import generate_jwt_token,verify_token,generate_jwt_token_only
from constants import SENDERID, SMS_AUTH_KEY, SMS_URL

from users.utils import generate_jwt_token
# local imports

from .tokens import account_activation_token
from users.models import *
from users.api.serializers import *
from users.utils import generate_jwt_token, TwilioAPI
from users.models import User



class GetOtp(APIView):
    permission_classes = (AllowAny,)
    serializer_class = OtpSerializer
    allowed_methods = ('POST',)

    def send_otp(self, phone_number):
        # import pdb;pdb.set_trace()

        otp = random.choice(range(11111,99999))
        twilio_api = TwilioAPI()
        message = "Your Otp: %s" %(otp)
        response = twilio_api.send_message(phone_number, '+18884420252', message)
        response['otp'] = otp
        return response

    def post(self, request, *args, **kwargs):
        # import pdb;pdb.set_trace()
        data = request.data
        serializer = OtpSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.data['phone_number']
            response = self.send_otp(phone_number)
            
            if response.get('status'):
                OTP_Data.objects.create(otp=response['otp'],phone_number=phone_number)
                return Response({'message':'Successfully Send Otp to your phone'}, status=status.HTTP_201_CREATED)
           
            else:
                return Response({'message':'Error In message Send Please try again'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message':'Successfully Send Otp to your phone'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOtp(APIView):
    permission_classes = (AllowAny,)
    serializer_class = VerifyOtpSerializer
    allowed_methods = ('POST',)
    # import pdb;pdb.set_trace()
    def get_otp_record(self, otp, phone_number):
        
        try:
            otpRecord = OTP_Data.objects.get(otp=otp, phone_number=phone_number)
            if otpRecord and (otpRecord.created).time()>(datetime.datetime.now() - datetime.timedelta(hours = 1)).time():
                return True
        except:
            pass
        return False

    def post(self, request, *args, **kwargs):
        serializer = VerifyOtpSerializer(data=request.data)
       
        if serializer.is_valid():
            phone_number = serializer.data['phone_number']
            otp = serializer.data['otp']

            return Response({'status':self.get_otp_record(otp, phone_number)}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SignupAPIView(APIView):
    serializer_class = UserSignupSerializer
    allowed_methods = ('POST',)
    permission_classes = (AllowAny,)    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # user = serializer.create(serializer.data)
            #user_detail_serializer = UserDetailSerializer(user)
            data = generate_jwt_token(user, serializer.data)
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):    
    serializer_class = JSONWebTokenSerializer
    permission_classes = (AllowAny,)
    allowed_methods = ('POST',)
    def post(self, request, *args, **kwargs):
        serializer = JSONWebTokenSerializer(data=request.data)
        if serializer.is_valid():
            serialized_data = serializer.validate(request.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestAppAPIView(APIView):

    def get(self, request, format=None):
        try:
            result = add.delay(11, 15)
            print(result)
            return Response({'status': True,
                             'Response': "Successfully Tested"},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class UserListmy(generics.ListAPIView):
    
    serializer_class = UserCreateSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        name = self.request.user
        return User.objects.filter(name=name)



class RegistrationAPIView(GenericAPIView):
   
    
    serializer_class = UserCreateSerializer

    __doc__ = "Registration API for user"

    def post(self, request, *args, **kwargs):

        try:
            user_serializer = UserCreateSerializer(data=request.data)
            
            if user_serializer.is_valid():
                user_serializer.is_active = False
                user = user_serializer.save()
                data = generate_jwt_token(user, user_serializer.data)
                #send_verification_email.delay(user.pk)
                current_site = get_current_site(request)
                if user.email:
                    subject = 'Thank you for registering to our site'
                    message = render_to_string('send/index2.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                        'token':account_activation_token.make_token(user),
                    })
                    from_email = settings.EMAIL_HOST_USER
                    recipient_list = [user.email,]
                    send_mail( subject=subject, message=message, from_email=from_email, recipient_list=recipient_list,fail_silently=False )
             
                return Response(data, status=status.HTTP_200_OK)

            else:
                message = ''
                for error in user_serializer.errors.values():
                    message += " "
                    message += error[0]
                return Response({'status': False,
                                 'message': message},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)


class ActivateApi(GenericAPIView):
    
    serializer_class = UserCreateSerializer
    
    __doc__ = "Activation API for user"

    def get( self, request, uidb64, token):
        try:
            
            #user_serializer = UserCreateSerializer(data=request.data)
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            LoginView(self,request, user)
        # return redirect('home')
            return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        else:
            return HttpResponse('Activation link is invalid!')

class Verify(GenericAPIView):       
 
    serializer_class = UserCreateSerializer
    def get(request, uuid):
        try:
            user = User.objects.get(verification_uuid=uuid, is_verified=False)
        except User.DoesNotExist:
            raise Http404("User does not exist or is already verified")
 
        user.is_verified = True
        user.save()



class LoginView(JSONWebTokenAPIView):
    serializer_class = JSONWebTokenSerializer
    
    __doc__ = "Log In API for user which returns token"

    @staticmethod
    def post(request):
    
        try:
            serializer = JSONWebTokenSerializer(data=request.data)
            if serializer.is_valid():
               
                serialized_data = serializer.validate(request.data)
                user = User.objects.get(phone_number=request.data.get('phone_number'))
                return Response({
                    'status': True,
                    'token': serialized_data['token'],
                }, status=status.HTTP_200_OK)
                
            else:
                message = ''
                for error in serializer.errors.values():
                    message += " "
                    message += error[0]
                return Response({'status': False,
                                 'message': message},
                                status=status.HTTP_400_BAD_REQUEST)


        except (AttributeError, ObjectDoesNotExist):
            return Response({'status': False,
                             'message': "User doesnot exists"},
                            status=status.HTTP_400_BAD_REQUEST)



class LogoutView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        """
        Logout API for user
        """
        try:
            user = request.data.get('user', None)
            logout(request)
            return Response({'status': True,
                             'message': "logout successfully"},
                            status=status.HTTP_200_OK)
        except (AttributeError, ObjectDoesNotExist):
            return Response({'status': False},
                            status=status.HTTP_400_BAD_REQUEST)


class UserAPIView(GenericAPIView):
    serializer_class = UserListSerializer
    # permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        """
        List all the users.
        """
        try:
            users = User.objects.all()
            user_serializer = UserListSerializer(users, many=True)

            users = user_serializer.data
            return Response({'status': True,
                             'Response': users},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class RefreshJwtToken(APIView):    
    serializer_class = RefreshTokenSerializer
    permission_classes = (AllowAny,)
    allowed_methods = ('POST',)
    def post(self, request, *args, **kwargs): 
        # import pdb;pdb.set_trace()
        serializer = JSONWebTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(phone_number=request.data['phone_number']) or request.user
            check_pwd = user.check_password(request.data['password'])
            if user and check_pwd:
                try:
                    token = verify_token(request.data['existing_token']) 
                    # import pdb;pdb.set_trace()  
                    if not token['status']:
                        if token['msg'] == 'Signature has expired.':
                            data = generate_jwt_token_only(user)
                            return Response({'New Token':data}, status=status.HTTP_200_OK)
                        else:
                            return Response({'msg':'Only Expired and Valid tokens can be refreshed.'}, status=status.HTTP_200_OK)
                    else:
                        return Response({'msg':'No need to refresh current token.'}, status=status.HTTP_200_OK)
                except:
                    return Response({'msg':'Wrong Json Request.'}, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({'msg':'Wrong Credentials.'}, status=status.HTTP_200_OK)

            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class Test1(APIView):
#     authentication_classes = (JSONWebTokenAuthentication,)
#     permission_classes = (AllowAny,)
#     allowed_methods = ('POST',)
#     def post(self, request, *args, **kwargs):
#        return Response({'msg':True}, status=status.HTTP_200_OK)