from rest_framework import serializers

from contacts.models import Contact


class ContactSerializer(serializers.ModelSerializer):
    contact = serializers.RelatedField()

    class Meta:
        model = Contact
        fields = ('id', 'first_name', 'last_name', 'phone_number')
