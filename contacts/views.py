from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from contacts.models import Contact
from contacts.serializers import ContactSerializer

class ContactList(generics.ListCreateAPIView):
    model = Contact
    serializer_class = ContactSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)

    def pre_save(self, obj):
        obj.user = self.request.user

class ContactDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Contact
    serializer_class = ContactSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)
