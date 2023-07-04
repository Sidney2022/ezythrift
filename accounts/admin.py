from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile


class ProfileAdmin(UserAdmin):
    model = Profile
    list_display = [ 'username', 'email', 'first_name', 'last_name', 'is_staff',  'last_login']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ( 'country', 'state', 'city', 'address', 'apartment', 'phone_number')}),
    )
    

# class NotificationAdmin(admin.ModelAdmin):
#     list_display = ['user', 'message', 'icon', 'timestamp']


admin.site.register(Profile, ProfileAdmin)
# admin.site.register(Notification, NotificationAdmin)





