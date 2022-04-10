from django.shortcuts import render, get_object_or_404
import requests
from constants import SENDERID, SMS_AUTH_KEY, SMS_URL
import json
import random
# from django.core.urlresolvers import reverse

from django.contrib import messages
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.shortcuts import redirect ,render
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

# from user.tasks import create_random_user_accounts
from django.db.models import Q
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import get_user_model
from django.views.generic import ListView
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from users.forms import LoginForm, UserForm
from users.models import OTP_Data, UserProfile ,Wallet
from users.utils import generate_jwt_token
from users.api.tokens import account_activation_token
from books.models import Books, BooksDetail, Author, BookCategory
from suppliers.models import Suppliers
from cart.models import CartData
from cart.cart import Cart
from cart.views import cart_add
from cart.forms import CartAddProductForm
from .models import User

User = get_user_model()


class UsersListView(ListView):
    template_name = 'user/users_list.html'
    model = User

class cartItem():
    price = ''
    name = ''
    isbn_code = ''
    book_condition = ''
    image = ''

def login_user(request):
    context={}
    try :
        if request.method == 'POST':
            
            form = LoginForm(request.POST)

            if form.is_valid(): 
                # form.save() 

                phone_number = request.POST.get('countries')+request.POST.get('phone_number')
                password = request.POST.get('password')
                user = authenticate(phone_number=phone_number, password=password)
                auth_login(request, user ,backend='django.contrib.auth.backends.ModelBackend')
                if (user.user_type=='user'):
                    if CartData.objects.filter(user=request.user):
                        cart_obj      = CartData.objects.filter(user=request.user)
                        cart_list = []
                        total_price = 0
                        item_count = 0
                        for cart_item in cart_obj[0].book_info:
                            for i in range(cart_item['quantity']):
                                total_price += cart_item['price']
                            item_count += cart_item['quantity']
                            obj = cartItem()
                            obj.price = cart_item['price']
                            obj.name = cart_item['book_name']
                            obj.isbn_code = cart_item['isbn_code']
                            obj.image = cart_item['image']
                            obj.book_condition = cart_item['book_condition']
                            cart_list.append(obj)
                        return render(request, "index1.html",{'cart':cart_list,'by_view':True,'total':total_price,'ccount':item_count})
                    else:
                        return HttpResponseRedirect('/')
                    # return HttpResponseRedirect('/')
                elif (user.user_type=='supplier'):
                    
                    data = Suppliers.objects.get(user=request.user)
                    return redirect('/suppliers/home/',{'key':data})
                    # return HttpResponseRedirect('/suppliers/home/')
                return HttpResponseRedirect('/')    
                
            else:
                context["form"]= form

                return render(request, "registration/login_user.html",context)

        else:
            form = LoginForm()
            cart_obj      = CartData.objects.filter(user=request.user)
            cart_list = []
            total_price = 0
            item_count = 0
            for cart_item in cart_obj[0].book_info:
                for i in range(cart_item['quantity']):
                    total_price += cart_item['price']
                item_count += cart_item['quantity']
                obj = cartItem()
                obj.price = cart_item['price']
                obj.name = cart_item['book_name']
                obj.isbn_code = cart_item['isbn_code']
                obj.image = cart_item['image']
                obj.book_condition = cart_item['book_condition']
                cart_list.append(obj)

        return render(request, "registration/login_user.html", {'cart':cart_list,'by_view':True,'total':total_price,'ccount':item_count})
    except:    
        context["error"] = "please Insert Your MobileNumber or password!"
        return render(request, "registration/login_user.html",context)


def register_user(request):
    context={}
    if request.method == 'POST':
        form = UserForm(request.POST)
        # context["form"]= form
        if form.is_valid():
            
            user=form.save()
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            phone_number = form.cleaned_data.get('phone_number')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(phone_number=phone_number, password=raw_password)
            login(request, user)
            
            return HttpResponseRedirect('/')

        else:
            context["error"] = "this phone_number is already present"
            return render(request,"registration/register_user.html", context)    
    else:
        form = UserForm()
    return render(request, "registration/register_user.html", {'form': form})

def SignUp(request):
    context={}
    
    try:
        
        if request.method == 'POST':
            # import pdb;pdb.set_trace()
            form = UserForm(request.POST)
            
            if form.is_valid():
                
                user=form.save()
                user.set_password(form.cleaned_data.get('password'))
                user.save()
                if(user.user_type=="user"):
                    wallet =Wallet.objects.create(user= user )
                    user=UserProfile.objects.create(user= user ,wallet =wallet)
                    user.save()
                
                    try:
                        current_site = get_current_site(request)
                        if user.email:
                            subject = 'Activate Your MySite Account'
                            message = render_to_string('email_send/acc_active_email.html', {
                                'user': user,
                                'domain': current_site.domain,
                                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                                'token': account_activation_token.make_token(user),
                 

                            })
                            from_email = settings.EMAIL_HOST_USER
                            recipient_list = [user.email,]
                            send_mail( subject=subject, message=message, from_email=from_email, recipient_list=recipient_list,fail_silently=False )
                        phone_number = form.cleaned_data.get('phone_number')
                        raw_password = form.cleaned_data.get('password')
                        user = authenticate(phone_number=phone_number, password=raw_password)
                        return HttpResponseRedirect('/')
                    except:
                        pass        
                   
                elif(user.user_type=="supplier"):   
                    wallet =Wallet.objects.create(user= user )
                    user=Suppliers.objects.create(user=user, wallet=wallet)
                    user.save()
                   
                    return HttpResponseRedirect('/suppliers/home/')
                else:
                    return HttpResponseRedirect('/')

            else:
                context['form'] = form
                # context["error"] = "this phone_number is already Register"
                return render(request, "registration/signup.html", context)    
        else:
            form = UserForm()
        return render(request, 'registration/signup.html', {'form': form})
    except:
        context["error"] = "Please insert the data!"
        return render(request, 'registration/signup.html', context)    



def account_activation_sent(request):

    return render(request, 'registration/signup.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        # user.profile.email_confirmed = True
        user.save()
        # phone_number = form.cleaned_data.get('phone_number')
        # raw_password = form.cleaned_data.get('password')
        # user = authenticate(phone_number=phone_number, password=raw_password)
        
        login(request, user)
        return redirect('/')
    else:
        return render(request, 'email_send/acc_active_email.html')



def Logout(request):
   
    logout(request)
    return HttpResponseRedirect('/')


def upload(request):
    if  request.method =='POST':
        upload_file = request.FILES['document']
        print(upload_file.name)
        print(upload_file.size)
    return render(request,"upload.html")


def user_profile(request , phone_number):
    data = User.objects.get(phone_number=phone_number)

    return render(request, 'registration/profile.html',{'data':data})



def find_books(request):

    if request.method=='POST':

        sr =request.POST['srch']

        if sr:
            match = Books.objects.filter(Q(book_name__icontains=sr))

            if match:
                return render(request,'find_book.html', {'match':match})
            else:
                messages.error(request, 'no result found')
        else:
            return HttpResponseRedirect('/')
    # return render(request, 'search.html')
    return render(request, 'find_book.html')

def find_book(request):
    # import pdb;pdb.set_trace()
    if request.method=='POST':
        sr =request.POST['key']
        ss =request.POST['srch']

        if sr:
            match = Books.objects.filter(Q(book_name__icontains=sr))
            if ss:
                match = Books.objects.filter(Q(book_name__icontains=sr)|Q(author_id__name__icontains=ss))
                return render(request,'find_book.html', {'match':match})
            elif match:
                return render(request,'find_book.html', {'match':match})
            else:
                messages.error(request, 'no result found')
        elif ss:
            match = Books.objects.filter(Q(author_id__name__icontains=ss))

            if match:
                return render(request,'find_book.html', {'match':match})
            else:
                messages.error(request, 'no result found')

        else:
            messages.error(request, 'no result found')
    # return render(request, 'search.html')
    return render(request, 'find_book.html', {})


def new_search(request, isbn_code=None):
    # import pdb;pdb.set_trace()
    users= User.objects.all()
    category = None
    categories = BookCategory.objects.all()
    books = Books.objects.all()
    book_groups = []
    book_list = []
    if isbn_code:
        category = get_object_or_404(BookCategory, id=isbn_code)
        books = books.filter(category_id=category)
    for book in books:
        book_list.append(book)
        if len(book_list) == 4:
            book_groups.append(book_list)
            book_list = []

    

    return render(request, 'home/search_index.html', {'user': users, 'category': category,
                                                      'categories': categories,
                                                      'books': book_groups})


