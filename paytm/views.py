from django.shortcuts import render
from django.http import HttpResponse
from django.utils.translation import get_language
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from orders.models import OrderAddress
from django.shortcuts import render, get_object_or_404

from decimal import Decimal
# from . import Checksum


from paytm.models import PaytmHistory
# Create your views here.

# @login_required
def home(request):

    return HttpResponse("<html><h2>Please select the payment option</h2><ul><li><a href='"+ settings.HOST_URL +"/paytm/payment/'><button>Paytm</button></a></li></br><li><a href='"+ settings.HOST_URL +"/payment/process/'><button>PayPal</button></a></li></br><li><a href='"+ settings.HOST_URL +"/payment/'><button>Payumoney</button></a></li></br><li><a href='"+ settings.HOST_URL +"/payu/'><button>Payu</button></a></li></ul></html>")

def payment(request):
    # import pdb; pdb.set_trace()
    MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
    MERCHANT_ID = settings.PAYTM_MERCHANT_ID
    get_lang = "/" + get_language() if get_language() else ''
    CALLBACK_URL = settings.HOST_URL + get_lang + settings.PAYTM_CALLBACK_URL
    # Generating unique temporary ids
    order_id = request.session.get('order_id')
    order = get_object_or_404(OrderAddress, id=order_id)

    bill_amount = 100
    if bill_amount:
        data_dict = {
                    'MID':MERCHANT_ID,
                    'ORDER_ID':order_id,
                    'TXN_AMOUNT': "1000",
                    'CUST_ID':'navincollexatech@gmail.com',
                    'INDUSTRY_TYPE_ID':'Retail',
                    'WEBSITE': settings.PAYTM_WEBSITE,
                    'CHANNEL_ID':'WEB',
                    #'CALLBACK_URL':CALLBACK_URL,
                }
        param_dict = data_dict
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(data_dict, MERCHANT_KEY)
        return render(request,"payment/payment.html",{'paytmdict':param_dict})
    return HttpResponse("Bill Amount Could not find ")


@csrf_exempt
def response(request):
    if request.method == "POST":
        MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
        data_dict = {}
        for key in request.POST:
            data_dict[key] = request.POST[key]
        verify = Checksum.verify_checksum(data_dict, MERCHANT_KEY, data_dict['CHECKSUMHASH'])
        if verify:
            PaytmHistory.objects.create(user=request.user, **data_dict)
            return render(request,"response.html",{"paytm":data_dict})
        else:
            return HttpResponse("checksum verify failed")
    return HttpResponse(status=200)