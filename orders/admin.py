from django.contrib import admin

# Register your models here.
from orders.models import OrderAddress, OrderDetail

# class OrderAdmin(admin.ModelAdmin):
#     list_display = ['customer_id', 'status', 'order_date']

admin.site.register(OrderAddress)
admin.site.register(OrderDetail)