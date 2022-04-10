from django.shortcuts import render
from cart.models import CartData

# Create your views here.
class cartItem():
    price = ''
    name = ''
    isbn_code = ''
    book_condition = ''
    image = ''
    
    def home(request):
        # if request.user.is_authenticated():
        #     if CartData.objects.filter(user=request.user):
        #         cart_obj      = CartData.objects.filter(user=request.user)
        #         cart_list = []
        #         total_price = 0
        #         item_count = 0
        #         for cart_item in cart_obj[0].book_info:
        #             for i in range(cart_item['quantity']):
        #                 total_price += cart_item['price']
        #             item_count += cart_item['quantity']
        #             obj = cartItem()
        #             obj.price = cart_item['price']
        #             obj.name = cart_item['book_name']
        #             obj.isbn_code = cart_item['isbn_code']
        #             obj.image = cart_item['image']
        #             obj.book_condition = cart_item['book_condition']
        #             cart_list.append(obj)

        #         return render(request, "index1.html",{'cart':cart_list,'by_view':True,'total':total_price,'ccount':item_count})
        #     else:
        #         return render(request, "index1.html")
        # else:
        #     return render(request, "index1.html")
        return render(request, "index1.html")    