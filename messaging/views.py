from django.db.models import Q

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from messaging.models import Message
from messaging.serializers import MessageSerializer

from contacts.models import Contact


class MessageList(generics.ListCreateAPIView):
    model = Message
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user

        qs = Message.objects.filter(user=user)

        contact_id = self.request.GET.get('contact')

        if contact_id:
            contact = Contact.objects.get(pk=contact_id)

            qs = qs.filter(Q(recepient=contact) | Q(sender=contact))

        return qs.order_by('id')

    def pre_save(self, obj):
        obj.user = self.request.user

    def post_save(self, obj, created):
        obj.send()

class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Message
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user

        return Message.objects.filter(user=user)
