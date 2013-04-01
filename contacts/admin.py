from django.contrib import admin

from contacts.models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name', 'phone_number']

admin.site.register(Contact, ContactAdmin)
