from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from books.models import Books, BookCategory ,Author
from .forms import BookForm
from suppliers.models import SupplierBooks, Suppliers
# Create your views here.

def supplierhome(request, *args, **kwargs):
      
    try:
        data1 = Suppliers.objects.filter(user=request.user.id)
        data2 = SupplierBooks.objects.filter(supplier=Suppliers.objects.get(user=request.user.id))
        return render(request, 'supplier/supplier_home.html' , {"data":data1, "val":data2}) 
    except:
        return HttpResponseRedirect('/')

def insert_book(request):
    context={}
    
    try:
        if request.method == 'POST':

            form = BookForm(request.POST)
            supplier = request.POST.get('supplier') 
            isbn_code = request.POST.get('isbn_code')
            book_name = request.POST.get('book_name')
            image = request.POST.get('image')
            mrp = request.POST.get('mrp')
            binding_type = request.POST.get('binding_type')
            language = request.POST.get('language')
            book_description = request.POST.get('book_description')
            category = request.POST.get('category')
            author = request.POST.get('author')
            buy_count = request.POST.get('buy_count')
            rent_count = request.POST.get('rent_count')
            book_condition = request.POST.get('book_condition')
            publication_year = request.POST.get('publication_year')
            
            if form.is_valid():    
                # import pdb;pdb.set_trace()
                book_isbn=Books.objects.filter(isbn_code=isbn_code)
                author_data=Author.objects.filter(name=str(author))
                for i in author_data:
                    i.name
                    author_data=i.name
                book_cate=BookCategory.objects.filter(genre=str(category))
                for cate in book_cate:
                    cate.genre
                    book_cate=cate.genre
                if (isbn_code!=book_isbn):
                # if (isbn_code!=book_isbn|author!=author_data|category!=category):
                # if isbn_code!=Books.objects.filter(isbn_code=isbn_code):   
                    try:
                        if(author!=author_data):
                            author = Author.objects.create(name=author)
                        # if(author!=author_data):
                        else:
                            author = Author.objects.get(name=author_data)
                        
                        if(category!=book_cate):
                            category = BookCategory.objects.create(genre=category)
                        else :    
                            category = BookCategory.objects.get(genre=category)
                        Books.objects.create(isbn_code=isbn_code,
                            book_name=book_name, image=image, mrp=mrp, binding_type=binding_type,
                            language=language, book_description=book_description, 
                            author_id=author, category_id=category, buy_count=buy_count,rent_count=rent_count,
                            book_condition=book_condition, publication_year=publication_year) 
                        form.save()  
                    except:

                        form.save()  
                return HttpResponseRedirect('/suppliers/home/')

            else:
                context["error"] = "already present"
                return redirect('/suppliers/home/',context)
                # HttpResponseRedirect('/suppliers/home/')
                
                # return render(request,'supplier/supplier_home.html', context) 
        else:
            form = BookForm()
        return render(request, 'supplier/supplier_home.html')
    except :
        
        return HttpResponseRedirect('/suppliers/home/')



def update_book(request, isbn_code):
    # import pdb;pdb.set_trace()
    s_book = get_object_or_404(SupplierBooks, isbn_code= isbn_code)
    
    if request.method == 'POST':
        
        s_book.isbn_code = request.POST['isbn_code']
        s_book.book_name = request.POST['book_name']
        s_book.image = request.POST['image']
        s_book.mrp = request.POST['mrp']
        s_book.binding_type = request.POST['binding_type']
        s_book.language = request.POST['language']
        s_book.book_description = request.POST['book_description']
        s_book.category = request.POST['category']
        s_book.author = request.POST['author']
        s_book.buy_count = request.POST['buy_count']
        s_book.rent_count = request.POST['rent_count']
        s_book.book_condition = request.POST['book_condition']
        s_book.publication_year = request.POST['publication_year']
        
        s_book.save()
        return HttpResponseRedirect("/suppliers/home/")  
        
    else:
        return render (request, 'supplier/supplier_add_book.html' ,{"key":s_book})
    
        
    return render (request, 'supplier/supplier_add_book.html' ,{"key":s_book})
    


def delete_book(request, isbn_code):
   # import pdb;pdb.set_trace()
   s_book = SupplierBooks.objects.filter(isbn_code = isbn_code)
   s_book.delete()
   return HttpResponseRedirect('/suppliers/home/')