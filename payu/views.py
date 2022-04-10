from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context, Template,RequestContext
import datetime
import hashlib
import random 
from random import randint
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from orders.models import OrderAddress
# from django.core.context_processors import csrf

def Home(request):
    # import pdb;pdb.set_trace()
    MERCHANT_KEY = "JBZaLc"
    key="JBZaLc"
    MERCHANT_SALT = "GQs7yium"
    PAYU_BASE_URL = "https://sandboxsecure.payu.in/_payment"
    action = 'https://test.payu.in/_payment'
    posted={}
    # Merchant Key and Salt provided by the PayU.
    for i in request.POST:
        posted[i]=request.POST[i]
    hash_object = hashlib.sha256(b'randint(0,20)')
    txnid=hash_object.hexdigest()[0:20]
    hashh = ''
    order_id = request.session.get('order_id')
    order = get_object_or_404(OrderAddress, id=order_id)
    posted['txnid']=txnid
    posted['amount']='%.2f' % order.get_total_cost()
    posted['productinfo']=request.GET.get('productinfo')
    posted['firstname']=request.GET.get('firstname')
    posted['email']=request.GET.get('email')

    hashSequence = "key|txnid|amount|productinfo|firstname|email"
    posted['key']=MERCHANT_KEY
    hash_string=''
    hashVarsSeq=hashSequence.split('|')
    for i in hashVarsSeq:
        try:
            hash_string+=str(posted[i])
        except Exception:
            hash_string+=''
        hash_string+='|'
    # import pdb;pdb.set_trace()
    hash_string+=MERCHANT_SALT
    posted['hashh']=hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest()
    action =PAYU_BASE_URL
    if(posted.get("key")!=None and posted.get("txnid")!=None and posted.get("amount")!=None and posted.get("productinfo")!=None and posted.get("firstname")!=None and posted.get("email")!=None):
        return render(request, 'payu/current_datetime.html',
                                {"posted":posted,
                                "MERCHANT_KEY":MERCHANT_KEY,
                                "hash_string":hash_string,
                                "action":"https://test.payu.in/_payment/"})
    else:
        return render(request, 'payu/current_datetime.html', {"posted":posted, "action":"https://test.payu.in/_payment/" })

@csrf_protect
@csrf_exempt
def success(request):
    c = {}
    c.update(csrf(request))
    status=request.POST["status"]
    firstname=request.POST["firstname"]
    amount=request.POST["amount"]
    txnid=request.POST["txnid"]
    posted_hash=request.POST["hash"]
    key=request.POST["key"]
    productinfo=request.POST["productinfo"]
    email=request.POST["email"]
    salt="GQs7yium"
    try:
        additionalCharges=request.POST["additionalCharges"]
        retHashSeq=additionalCharges+'|'+salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
    except Exception:
        retHashSeq = salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
    hashh=hashlib.sha512(retHashSeq).hexdigest().lower()
    if(hashh !=posted_hash):
        print("Invalid Transaction. Please try again")
    else:
        print("Thank You. Your order status is ", status)
        print("Your Transaction ID for this transaction is ",txnid)
        print("We have received a payment of Rs. ", amount ,". Your order will soon be shipped.")
    return render_to_response('payu/success.html',RequestContext(request,{"txnid":txnid,"status":status,"amount":amount}))


@csrf_protect
@csrf_exempt
def failure(request):
    c = {}
    c.update(csrf(request))
    status=request.POST["status"]
    firstname=request.POST["firstname"]
    amount=request.POST["amount"]
    txnid=request.POST["txnid"]
    posted_hash=request.POST["hash"]
    key=request.POST["key"]
    productinfo=request.POST["productinfo"]
    email=request.POST["email"]
    salt=""
    try:
        additionalCharges=request.POST["additionalCharges"]
        retHashSeq=additionalCharges+'|'+salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
    except Exception:
        retHashSeq = salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
    hashh=hashlib.sha512(retHashSeq).hexdigest().lower()
    if(hashh !=posted_hash):
        print("Invalid Transaction. Please try again")
    else:
        print("Thank You. Your order status is ", status)
        print("Your Transaction ID for this transaction is ",txnid)
        print("We have received a payment of Rs. ", amount ,". Your order will soon be shipped.")
    return render_to_response("payu/Failure.html",RequestContext(request,c))

    
