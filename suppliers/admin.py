from django.contrib import admin

# Register your models here.
from suppliers.models import Suppliers, Shop, SupplierBooks

class SuppliersAdmin(admin.ModelAdmin):
	list_display = ['user','wallet']

admin.site.register(Suppliers,SuppliersAdmin)
admin.site.register(Shop)
admin.site.register(SupplierBooks)
