# from django.shortcuts import render
# import requests
# from constants import SENDERID, SMS_AUTH_KEY, SMS_URL
# import json
# import random
# # from django.core.urlresolvers import reverse
# from .models import User
# from django.contrib import messages
# from django.views.generic import TemplateView
# from django.views.generic.list import ListView
# from django.views.generic.edit import FormView
# from django.shortcuts import redirect
# from django.contrib.auth import authenticate, login, logout
# # from user.tasks import create_random_user_accounts
# from django.db.models import Q
# from django.shortcuts import render
# from django.http import HttpResponseRedirect,HttpResponse
# from django.contrib.auth.models import User
# from django.contrib.auth import login as auth_login
# from user.forms import LoginForm, UserForm
# from django.views.generic import ListView
# from user.models import OTP_Data
# from user.utils import generate_jwt_token
# from django.contrib.auth import get_user_model


# class UsersListView(ListView):
#     template_name = 'user/users_list.html'
#     model = User

# def login(request):
   
#     context={}
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         context["form"]= form
        
#         if form.is_valid(): 
#             # form.save()           
#             phone_number = form.cleaned_data.get('phone_number')
#             password = form.cleaned_data.get('password')
#             user = authenticate(phone_number=phone_number, password=password)
#             auth_login(request, user)
#             return HttpResponseRedirect('/')

#         else:
#             context["error"] = "Please enter correct phone_number and password"
#             return render(request, "registration/login.html", context)

#     else:
#         form = LoginForm()
#         return render(request, "registration/login.html",{'form': form})

# def main(request):


#     return render(request, "main.html")



# def SignUp(request):
#     context={}
#     if request.method == 'POST':
        
#         form = UserForm(request.POST)
#         context["form"]= form
#         if form.is_valid():
            
#             user=form.save()
#             user.set_password(form.cleaned_data.get('password'))
#             user.save()
#             phone_number = form.cleaned_data.get('phone_number')
#             raw_password = form.cleaned_data.get('password')
#             user = authenticate(phone_number=phone_number, password=raw_password)
#             login(request)
            
#             return HttpResponseRedirect('/')

#         else:
#             context["error"] = "this phone_number is already present"
#             return render(request, "signup.html", context)    
#     else:
#         form = UserForm()
#     return render(request, 'signup.html', {'form': form})



# def LogOut(request):
   
#     logout(request)
#     return render(request, 'registration/login.html')


# def upload(request):
#     if  request.method =='POST':
#         upload_file = request.FILES['document']
#         print(upload_file.name)
#         print(upload_file.size)
#     return render(request,"upload.html")


# def user_profile(request , phone_number):
#     # import pdb;pdb.set_trace()

    
#     data = User.objects.get(phone_number=phone_number)

#     # return render(request, 'registration/profile.html',{'data':data})

#   