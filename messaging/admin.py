from django.contrib import admin

from messaging.models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'sender', 'recepient', 'message', 'date_sent']

admin.site.register(Message, MessageAdmin)
