from rest_framework import serializers

from messaging.models import Message


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.Field(source='get_sender')
    contact = serializers.Field(source='get_contact')

    class Meta:
        model = Message
        fields = ('id', 'sender', 'sender_name', 'recepient',
                  'contact', 'message', 'date_sent')
