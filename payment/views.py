import hashlib
from decimal import Decimal
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
# from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from paypal.standard.forms import PayPalPaymentsForm
#payumoney files
# from paywix.payu import PAYU
from random import randint
from transactions.models import Transactions
from users.api.tokens import account_activation_token
from orders.models import OrderAddress, OrderDetail
from books.models import Books
from suppliers.models import Suppliers, SupplierBooks
# from review.forms import ReviewForm
# from review.models import Review


@csrf_exempt
def payment_done(request):
    
    order_id = request.session.get('order_id')
    order = get_object_or_404(OrderAddress, id=order_id)
    order.status = 'Completed'
    order.save( )
    order_obj = OrderAddress.objects.filter(customer_id=request.user)
    for item in order_obj[0].order_info:
       isbn_code = item['isbn_code']
       book = get_object_or_404(Books,isbn_code=isbn_code)
       buy_count = book.buy_count
       book.buy_count = buy_count-1
       book.save()
    isbn = order_obj[0].order_info[0]['isbn_code']
    if buy_count < 10:
        try:
            suppiler =SupplierBooks.objects.filter(isbn_code=isbn)
            # print (supplier.supplier)
            for supplier_item in suppiler:
                supplier_book = supplier_item.book_name
                supplier_data = supplier_item.supplier
            # user=supplier_data.user   
            current_site = get_current_site(request)
            if supplier_data.user:
                subject = 'Activate Your MySite Account'
                message = render_to_string('email_send/email_send_supplier.html', {
                    'user': supplier_data,
                    # 'domain': current_site.domain,
                    # 'uid': urlsafe_base64_encode(force_bytes(supplier_data.pk)).decode(),
                    # 'token': account_activation_token.make_token(supplier_data),
                    'book_name':supplier_book,

                })
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [supplier_data.user,]
                send_mail( subject=subject, message=message, from_email=from_email, recipient_list=recipient_list,fail_silently=False )
        except:
            pass

    transactions = get_object_or_404(Transactions, order=order_id)
    transactions.status = 'success'
    transactions.save()
    return render(request, 'payment/done.html')


@csrf_exempt
def payment_canceled(request):
    # import pdb;pdb.set_trace()
    order_id = request.session.get('order_id')
    transactions = get_object_or_404(Transactions, order=order_id)
    transactions.status = 'failed'
    transactions.save()
    return render(request, 'payment/canceled.html')
    

def process(request):
    # import pdb;pdb.set_trace()
    order_id = request.session.get('order_id')
    order = get_object_or_404(OrderAddress, id=order_id)
    host = request.get_host()
    transaction = Transactions.objects.create(order=order,
                                                customer=request.user,
                                                transaction_date=timezone.now(),
                                                status='pending')
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % order.get_total_cost(),
        'item_name': 'Order {}'.format(order.id),
        'invoice': str(order.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('payment:done')),
        'cancel_return': 'http://{}{}'.format(host, reverse('payment:canceled')),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'payment/process.html', {'order': order,
                                                    'form':form})

        

# Import Payu from PAYWIX
# payu = PAYU()

# Intiate transaction
def checkout(request):
    # Creating unique Transaction ID(change as per your need)
    # import pdb;pdb.set_trace()
    hash_object = hashlib.sha256(b'randint(0,20)')
    txnid=hash_object.hexdigest()[0:20]
    order_id = request.session.get('order_id')
    order = get_object_or_404(OrderAddress, id=order_id)
    transaction = Transactions.objects.create(order=order,
                                                customer=request.user,
                                                transaction_date=timezone.now(),
                                                status='pending')
    # The below payment_data contains on the mandatory items

    payment_data = {
                    'txnid': txnid,
                    'amount': '%.2f' % order.get_total_cost(),
                    'firstname': 'Navin',
                    'email': 'wadbudenvn19@gmail.com',
                    'phone': '7566555545',
                    'productinfo': 'trust',
                   
    }

    # Once you make your Dict, Initiate with PAYU
    payu_data = payu.initate_transaction(payment_data)

    print('posted parameters are')
    print(payu_data)

    # The payu_data contains the input data for the pay payment data
    return render(request, 'payment/payment_form.html',{"posted":payu_data})

# Success URL
@csrf_protect
@csrf_exempt
def payment_success(request):
    # import pdb;pdb.set_trace()
    order_id = request.session.get('order_id')
    order = get_object_or_404(OrderAddress, id=order_id)
    order.status = 'success'
    order.save( )
    order_obj = OrderAddress.objects.filter(customer_id=request.user)
    for item in order_obj[0].order_info:
        isbn_code = item['isbn_code']
        book = get_object_or_404(Books,isbn_code=isbn_code)
        buy_count = book.buy_count
        book.buy_count = buy_count-1
        book.save()        
    
    transactions = get_object_or_404(Transactions, order=order_id)
    transactions.status = 'success'
    transactions.save()  

    payu_success_data = payu.check_hash(dict(request.POST))
    return render(request, 'payment/success_payu.html')


# Failure URL
@csrf_protect
@csrf_exempt

def payment_failure(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(OrderAddress, id=order_id)
    order.status = 'canceled'
    order.save( )
    transactions = get_object_or_404(Transactions, order=order_id)
    transactions.status = 'failed'
    transactions.save()
    return render(request, 'payment/Failure_payu.html')


    # current_site = get_current_site(request)
    #                     if user.email:
    #                         subject = 'Activate Your MySite Account'
    #                         message = render_to_string('email_send/acc_active_email.html', {
    #                             'user': user,
    #                             'domain': current_site.domain,
    #                             'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
    #                             'token': account_activation_token.make_token(user),
                 

    #                         })
    #                         from_email = settings.EMAIL_HOST_USER
    #                         recipient_list = [user.email,]
    #                         send_mail( subject=subject, message=message, from_email=from_email, recipient_list=recipient_list,fail_silently=False )