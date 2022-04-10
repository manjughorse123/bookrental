import json
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect 
from django.db.models import Q
from django.contrib import messages
from cart.models import CartData
from books.models import Books, Author
from django.contrib.auth.decorators import login_required
from cart.forms import CartAddProductForm, CartRentForm
from django.http import JsonResponse

def search(request):
    # import pdb;pdb.set_trace()
    if request.method=='POST':
        sr =request.POST['search']

        if sr:
            match = Books.objects.filter(Q(book_name__icontains=sr))

            if match:
                return render(request,'search.html', {'key':match})
            else:
                messages.error(request, 'no result found')
        else:
            return HttpResponseRedirect('/search/')
    return render(request, 'search.html')

def home(request):
    return render(request, 'search.html')


def auto_search(request):
   
    search =  request.GET.get('search','')
    books = Books.objects.filter(book_name__icontains=search)
    results = []

    for r in books:
       results.append(r.book_name)


    resp = json.dumps({'data':results})
    return HttpResponse(resp, content_type='application/json')


def author_search(request):
   
    search =  request.GET.get('search','')
    books = Author.objects.filter(name__icontains=search)
    results = []

    for r in books:
       results.append(r.name)


    resp = json.dumps({'data':results})
    return HttpResponse(resp, content_type='application/json')

    
class cartItem():
    price = ''
    name = ''
    isbn_code = ''
    book_condition = ''
    image = ''

@login_required(login_url="/users/login/")
def books_detail(request, isbn_code):
    books = get_object_or_404(Books, isbn_code=isbn_code)
    cart_books_form = CartAddProductForm()
    cart_books_rent_form = CartRentForm()

    if CartData.objects.filter(user=request.user):
        cartt      = CartData.objects.filter(user=request.user)
        cart_list = []
        total_price = 0
        item_count = 0
        for cart_item in cartt[0].book_info:
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

        return render(request,
                  'book_detail.html',
                  {'books': books,
                   'cart_books_form': cart_books_form,
                   'cart_books_rent_form':cart_books_rent_form, 'cart': cart_list, 'by_view':True,'total':total_price,'ccount':item_count})
    return render(request, 'book_detail.html', {'books':books, 'cart_books_form': cart_books_form, 'cart_books_rent_form': cart_books_rent_form})



def search1(request):

    results = []
    # import pdb;pdb.set_trace()
    if request.method=='GET':
        sr =request.GET.get('search', None)
        ss =request.GET.get('author',None)

        if sr:
            match = Books.objects.filter(Q(book_name__icontains=sr))
            if ss:
                match = Books.objects.filter(Q(book_name__icontains=sr)|Q(author_id__name__icontains=ss))
                # results = []
                for r in match:
                    results.append([r.book_name, r.image,r.author_id.name, float(r.mrp)])
                    resp = json.dumps({'data':results})
                # print(results)
                return HttpResponse(resp, content_type='application/json')
            elif match:
                # results = []
                for r in match:
                    results.append([r.book_name, r.image, r.author_id.name, float(r.mrp)])
                   
                    resp = json.dumps({'data':results})
                # print(resp)
                return HttpResponse(resp, content_type='application/json')
            else:
                messages.error(request, 'no result found')
        elif ss:

            match = match = Books.objects.filter(Q(author_id__name__icontains=ss))
            results =[]
            for r in match:
              results.append([r.book_name, r.image, r.author_id.name,float(r.mrp)])
              resp = json.dumps({'data':results})
              # print(results)
            return HttpResponse(resp, content_type='application/json')

            if match:
              results = []
              for r in match:
                results.append([r.book_name ,r.image, r.author_id.name,float(r.mrp)])
                resp = json.dumps({'data':results})

              return HttpResponse(resp, content_type='application/json')
            else:
                messages.error(request, 'no result found')

        else:
            messages.error(request, 'no result found')
    # return render(request, 'search.html')

    return HttpResponse(request, 'no result found')

def search2(request):
    # import pdb;pdb.set_trace()
    if request.method=='GET':
        sr =request.GET.get('search')
        
        if sr:
            match = Books.objects.filter(Q(book_name__icontains=sr))

            if match:
                
                # print (match)
                return render(request,'home/search_index.html', {'key':match})
            else:
                messages.error(request, 'no result found')
        else:
            return HttpResponseRedirect('/books/search/')
    return render(request, 'home/search_index.html')

def book_path(request):
    # import pdb;pdb.set_trace()
    if request.method=='GET':    
        isbn_code=request.GET.get('txt1')
        value = request.GET.get('value')
        book = get_object_or_404(Books, isbn_code=isbn_code)
        print('book_name:-',book)
        if value=='choose':
            price = float(book.mrp)
        elif value=='Rent 1-4days + Security':    
            price = (float(book.mrp)*30)/100+(float(book.mrp))
        elif value=='Rent 1week + Security 1week':
            price = (float(book.mrp)*20)/100+(float(book.mrp))
        elif value=='Rent 1month + Security':  
            price = (float(book.mrp)*15)/100+(float(book.mrp))
        elif value=='Rent 3months + Security':
            price = (float(book.mrp)*10)/100+(float(book.mrp))
        elif value=='Rent 1semester + Security':
            price = (float(book.mrp)*5)/100+(float(book.mrp))
        elif value=='Buy New':
            price = float(book.mrp)
        elif value=='Buy Used':
            price = (float(book.mrp)-10)
        else:
            print('please select right value')
        results = []
        results.append(price)
        resp = json.dumps({'data':results})
        print('price:-',price)
    return HttpResponse(resp, content_type='application/json')