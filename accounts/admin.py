from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile, Billing


class ProfileAdmin(UserAdmin):
    model = Profile
    list_display = [ 'username', 'email', 'first_name', 'last_name', 'is_staff',  'last_login']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ( 'country', 'state', 'city', 'address', 'apartment', 'phone_number')}),
    )
    

class BillingAdmin(admin.ModelAdmin):
    list_display = ['user', 'country', 'state', 'city']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Billing, BillingAdmin)





