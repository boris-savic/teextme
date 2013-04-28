from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.db.models import Q

from messaging.models import Message
from contacts.models import Contact

from messaging.forms import *


def messages_contact(request, contact_id):
    user = request.user

    qs = Message.objects.filter(user=user)

    if contact_id:
        contact = Contact.objects.get(pk=contact_id)

        qs = qs.filter(Q(recepient=contact) | Q(sender=contact))

    messages = qs.order_by('id')

    form = MessageForm(user=user, contact=contact)

    if request.method == 'POST':
        form = MessageForm(user=user, contact=contact, data=request.POST)
        if form.is_valid():
            form.save()

            return redirect('messages_contact', contact_id=contact_id)

    return render_to_response('messaging/messages.html', {
        'user': user,
        'contact_id': contact_id,
        'form': form,
        'messages': messages,
    }, RequestContext(request))
