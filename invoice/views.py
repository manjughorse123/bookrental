from django.shortcuts import render, get_object_or_404
# Create your views here.
from invoice.models import Invoice
from orders.models import OrderAddress

def InvoiceView(request, id):
	import pdb;pdb.set_trace()
	# invoice = Invoice.objects.all()
	order = get_object_or_404(OrderAddress, id=id) 
	invoice = Invoice.objects.create(order_id=order,
                                                user=request.user,)
	
    

	return render(request, "invoice/invoice.html" , {'invoices':invoice})




# def file_download(request):
   
#     filename = request.GET.get('filename')
#     with open(os.path.join(settings.BASE_DIR ,'crawler_output', filename), 'rb') as pdf:
#         response = HttpResponse(pdf.read())
#         response['content_type'] = 'application/pdf'
#         response['Content-Disposition'] = 'attachment;filename=%s' % filename
#         return response
#     return None