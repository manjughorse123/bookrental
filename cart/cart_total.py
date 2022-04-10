from django.conf import settings
from cart.models import CartData

class cartItem():
    price = ''
    name = ''
    isbn_code = ''
    book_condition = ''
    image = ''

    def cart_total(self):
        cart_list = []
        total_price = 0
        item_count = 0
        cartt      = CartData.objects.filter(user=request.user)
        for cart_item in cartt[0].book_info:
            total_price += cart_item['price']
            item_count += 1
            obj = cartItem()
            obj.price = cart_item['price']
            obj.name = cart_item['book_name']
            obj.isbn_code = cart_item['isbn_code']
            obj.image = cart_item['image']
            obj.book_condition = cart_item['book_condition']
            cart_list.append(obj)
        return total_price