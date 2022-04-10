from decimal import Decimal
from django.conf import settings
from books.models import Books
# from django.contrib.auth.decorators import login_required

class Cart(object):

    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):

        """
        Iterate over the items in the cart and get the products from the database.
        """
        isbn_code = self.cart.keys()
        # get the product objects and add them to the cart
        books = Books.objects.filter(isbn_code__in=isbn_code)
        for book in books:
            self.cart[str(book.isbn_code)]['book'] = book

        for item in self.cart.values():
            item['mrp'] = Decimal(item['mrp'])
            item['total_price'] = item['mrp'] * item['quantity']
            item['rent'] = Decimal(item['mrp'])
            yield item

    # @login_required(login_url="/users/login/")
    def add(self, book, quantity=1, update_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        book_isbn_code = str(book.isbn_code)
        if book_isbn_code not in self.cart:
            self.cart[book_isbn_code] = {'quantity': 0,
                                      'mrp': str(book.mrp)}
        if update_quantity:
            self.cart[book_isbn_code]['quantity'] = quantity
        else:
            self.cart[book_isbn_code]['quantity'] += quantity
        self.save()
        pass    
    def remove(self, book):
        """
        Remove a product from the cart.
        """
        book_isbn_code = str(book.isbn_code)
        if book_isbn_code in self.cart:
            del self.cart[book_isbn_code]
            self.save()

    def rent(self, book, days_for_rent=10):
        """
        Remove a product from the cart.
        """
        book_isbn_code = str(book.isbn_code)
        if book_isbn_code in self.cart:
            self.cart[book_isbn_code]['days_for_rent'] = days_for_rent
            self.save()


    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    # def delete(request):
    #     #delete the cart when user checkout
    #     request.session[settings.CART_SESSION_ID] = request.cart
    #     request.session.modified = True

    def clear(self):
        # empty cart
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True

    def get_total_price(self):
        return sum(Decimal(item['mrp']) * item['quantity'] for item in self.cart.values())

    def get_total_rent(self):
        return sum(Decimal(item['rent']) for item in self.cart.values())
