from django.contrib import admin


from users.models import User, Wallet, UserProfile

# Register your models here.

class UserAdmin(admin.ModelAdmin):
	list_display = ['phone_number','email','name', 'user_type']

admin.site.register(User, UserAdmin)
admin.site.register(Wallet)

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ['user','wallet']

admin.site.register(UserProfile,UserProfileAdmin)

