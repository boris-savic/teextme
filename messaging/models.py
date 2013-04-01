from django.db import models

from customauth.models import MyUser
from contacts.models import Contact

from teextme.sms import send_sms

class Message(models.Model):
    user = models.ForeignKey(MyUser)
    sender = models.ForeignKey(Contact, null=True, blank=True, related_name='sent_messages')
    recepient = models.ForeignKey(Contact, null=True, blank=True, related_name='received_messages')
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    date_received = models.DateTimeField(null=True, blank=True)
    other_message = models.ForeignKey('messaging.Message', null=True, blank=True, related_name='other_messages')

    def __unicode__(self):
        return self.message

    def send(self):
        sender_phone_number = self.user.full_number

        recepient_contact = self.recepient
        recepient_user = recepient_contact.contact_user
        recepient_phone_number = recepient_contact.phone_number

        if recepient_user: # recepient is registered in TeextMe
            sender_contact = Contact.objects.filter(contact_user=self.user)

            sender_contact = sender_contact[0] if sender_contact else None

            other_message = Message(
                user=self.recepient.contact_user,
                sender=sender_contact,
                message = self.message,
                date_sent = self.date_sent,
                other_message = self
            )

            other_message.save()

            self.other_message = other_message
        else:
            send_sms(sender_phone_number, recepient_phone_number, self.message)
