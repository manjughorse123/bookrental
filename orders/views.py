from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
# from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required 
from django.urls import reverse
from .models import OrderItem, OrderAddress  
from transactions.models import Transactions
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from cart.models import CartData
from books.models import Books


class cartItem():
    price = ''
    name = ''
    isbn_code = ''
    book_condition = ''
    image = ''
    
@login_required(login_url="/users/login/")
def order_create(request):
    # import pdb;pdb.set_trace()
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        customer_id=request.user
        cart_obj = get_object_or_404(CartData, user=request.user)
        order_info= cart_obj.book_info
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        postal_code = request.POST.get('postal_code')
        city = request.POST.get('postal_code')
        orders = OrderAddress.objects.create(customer_id=customer_id,order_info=order_info,first_name=first_name,email=email, address=address, postal_code=postal_code, city=city)
        orders.save()
        for item in cart:
            # OrderItem.objects.create(id=item['book'],
            #                          order_id=order,
            #                          price=item['mrp'],
            #                          quantity=item['quantity'])
            try:
                
                order_item = OrderItem()                    
                order_item.id = item['book']
                order_item.order_id = orders
                order_item.price = item['mrp']
                order_item.quantity = item['quantity']                   
                order_item.save()
                print('succeessfully saved')
            except:
                pass
        # clear the cart
        cart.clear()
        cart = CartData.objects.filter(user=request.user)
        cart.delete()
        # launch asynchronous task
        order_created(orders.id)
        # import pdb;pdb.set_trace()
        request.session['order_id'] = orders.id
        return redirect(reverse('paytm:home'))
    else:
        form = OrderCreateForm()
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
        return render(request, 'order_create.html', {'user':cart_obj, 'cart':cart_list,'by_view':True,'total':total_price,'ccount':item_count,'form':form})
    return render(request, 'order_create.html', {'user':cart_obj, 'cart':cart_list,'by_view':True,'total':total_price,'ccount':item_count,
                                                        'form': form})
class orderItem():
    items = ""
    mrp = ""
    book_name = ""
    total_count = ""
    image = ""
# Create your views here.
def myorders(request):

    if OrderAddress.objects.filter(customer_id=request.user):

        cart_obj      = OrderAddress.objects.filter(customer_id=request.user)
        cart_list = []
        for item in cart_obj:
            total_mrp = 0
            total_item = 0
            
            for item1 in item.order_info:
                total_item += 1
                total_mrp += item1['price']
                book_name  = item1['book_name']
                book = get_object_or_404(Books, book_name=book_name)
                images = book.image
            obj = orderItem()
            obj.items = item
            obj.total_count = total_item
            obj.mrp = total_mrp
            obj.book_name = book_name
            obj.image = images
            cart_list.append(obj)

    else:
        return render(request, "order_list.html")

    return render(request, "order_list.html", {'cart_dict':cart_list}) 

def myorders_detail(request, id):
    # import pdb;pdb.set_trace()
    orders = get_object_or_404(OrderAddress, id=id)
    total_mrp = 0
    total_item = 0
    cart_list = []
    for item in orders.order_info:
        total_item += 1
        total_mrp += item['price']
        book_name  = item['book_name']
        book = get_object_or_404(Books, book_name=book_name)
        images = book.image
    obj = orderItem()
    obj.items = orders
    obj.total_count = total_item
    obj.mrp = total_mrp
    obj.book_name = book_name
    obj.image = images
    cart_list.append(obj)

    return render(request, "order_detail.html", {'order':orders, 'cart':cart_list, 'id':id}) 

    # return render(request, "order_list.html", {'cart_dict':cart_list}) 

