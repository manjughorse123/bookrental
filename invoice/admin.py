from django.contrib import admin
from .models import Invoice, InvoiceItem

# class InvoiceAdmin(admin.ModelAdmin):
#     # list_display = ['invoice_num' ,'invoice_type' ,'invoice_status' ,'invoice_date' ,'payment_type' ,'user']
#     # list_filter = ['created', 'updated']
#     admin.site.register(Invoice, InvoiceAdmin)


# class InvoiceItemAdmin(admin.ModelAdmin):
#     # list_display = ['invoice' ,'item' ,'quantity' ,'discount' ,'cost']
#     # list_filter = ['created', 'updated']

#     admin.site.register(InvoiceItem, InvoiceItemAdmin)

admin.site.register(Invoice)
admin.site.register(InvoiceItem)
