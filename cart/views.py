from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST  
from books.models import Books
from cart.models import CartData
from .cart import Cart
from .forms import CartAddProductForm, CartRentForm
from django.contrib.auth.decorators import login_required
import json
from decimal import Decimal
import decimal
import copy 

@require_POST
@login_required(login_url="/users/login/")
def cart_add(request, isbn_code):
    # import pdb;pdb.set_trace()

    cart = Cart(request)
    book = get_object_or_404(Books, isbn_code=isbn_code)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(book=book,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    cart_data = copy.deepcopy(cart)
    # if cart_data:
    try:
        if CartData.objects.get(user=request.user):
            user_obj = CartData.objects.get(user=request.user)
            test = user_obj.book_info
            
            flag = False
            for i in range(len(test)):
                if test[i]['isbn_code'] == isbn_code:
                    if test[i]['quantity']>=1:
                        test[i]['quantity'] +=1
                        user_obj.save()
                        flag = True
                        break

            if flag ==False:
                cart_dict = {}
                cart_dict['quantity']   = 1
                cart_dict['type']       = 'Buy_type'
                cart_dict['isbn_code']          = book.isbn_code
                cart_dict['book_name']          = book.book_name
                cart_dict['image']              = book.image 
                cart_dict['book_condition']     = book.book_condition
                cart_dict['price']              = float(book.mrp)
                user_obj.book_info.append(cart_dict)
                user_obj.save()
                print('cart update')    

    except:
        cart_ad = CartData()
        try:
            cart_ad.user = request.user
            cart_ad.book_info = dict()
            cart_ad.book_info['quantity']   = 1
            cart_ad.book_info['type']       = 'Buy_type'
            cart_ad.book_info['isbn_code']  = book.isbn_code   
            cart_ad.book_info['book_name']  = book.book_name
            cart_ad.book_info['image']      = book.image       
            cart_ad.book_info['book_condition']  = book.book_condition 
            cart_ad.book_info['price']      =  float(book.mrp)                
            cart_list = []
            cart_list.append(cart_ad.book_info)
            cart_ad.book_info = cart_list


        except:
            pass

        cart_ad.save()            
        print("cart save to database")

    return redirect('cart:cart_detail')


def cart_remove(request, isbn_code=None):
    if isbn_code:
        if CartData.objects.filter(user=request.user):
            cart_obj = CartData.objects.get(user=request.user)
            test = cart_obj.book_info
            for i in range(len(test)):
                if test[i]['isbn_code']==isbn_code:
                    del test[i]
                    cart_obj.delete()
                    cart_obj1 = CartData()
                    cart_obj1.user = request.user
                    cart_obj1.book_info = test
                    cart_obj1.save()
                    print(test)
                    break

    return redirect('cart:cart_detail')

@login_required(login_url="/users/login/")  
def rent_book(request, isbn_code):
    # import pdb;pdb.set_trace()
    if request.method=='POST':
        mrp = request.POST.get('price')
        cart = Cart(request)
        book = get_object_or_404(Books, isbn_code=isbn_code)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(book=book,
                     quantity=cd['quantity'],
                     update_quantity=cd['update'])
        cart_data = copy.deepcopy(cart)
        if cart_data:
            try:
                if CartData.objects.get(user=request.user):
                    user_obj = CartData.objects.get(user=request.user)

                    cart_dict = {}
                    cart_dict['type']       = 'Rent_type'
                    cart_dict['isbn_code'] = book.isbn_code
                    cart_dict['book_name'] = book.book_name
                    cart_dict['image']      = book.image 
                    cart_dict['book_condition'] = book.book_condition
                    cart_dict['price'] = float(mrp)
                    user_obj.book_info.append(cart_dict)
                    user_obj.save()
                    print('cart update')    

            except:
                cart_ad = CartData()
                try:
                    cart_ad.user = request.user
                    cart_ad.book_info = dict()
                    cart_ad.book_info['quantity']   = 1
                    cart_ad.book_info['type']       = 'Rent_type'
                    cart_ad.book_info['isbn_code']  = book.isbn_code   
                    cart_ad.book_info['book_name']  = book.book_name
                    cart_ad.book_info['image']      = book.image       
                    cart_ad.book_info['book_condition']  = book.book_condition 
                    cart_ad.book_info['price']      =  float(mrp)                
                    cart_list = []
                    cart_list.append(cart_ad.book_info)
                    cart_ad.book_info = cart_list


                except:
                    pass

                cart_ad.save()            
                print("cart save to database")

    return redirect('cart:cart_detail')

class cartItem():
    price = ''
    name = ''
    isbn_code = ''
    book_condition = ''
    image = ''
def cart_detail(request):
    # import pdb;pdb.set_trace()
    cart = Cart(request)
    book = Books.objects.all()
    if CartData.objects.filter(user=request.user):
        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],'update': True})
        cart_list = []
        total_price = 0
        item_count = 0
        cart_obj = CartData.objects.filter(user=request.user)
        for cart_item in cart_obj[0].book_info:
            # total_price += cart_item['price']
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
        return render(request, 'cart_detail.html', {'book':book, 'carts':cart, 'cart': cart_list, 'by_view':True,'total':total_price,'ccount':item_count})
    return render(request, 'cart_detail.html', {'book':book, 'carts':cart})

