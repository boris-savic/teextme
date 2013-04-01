from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render_to_response

from django.template import RequestContext

from contacts.models import Contact

from contacts.forms import *


def index(request):
    
    user = request.user

    contacts = Contact.objects.filter(user=request.user)

    return render_to_response('contacts/index.html', {
        'user': user,
        'contacts': contacts,
        }, RequestContext(request))

def add_contact(request):

    if request.method == 'POST':
        form = ContactForm(user=request.user, data=request.POST)
        if form.is_valid():
            new_contact = form.save() #save
            return HttpResponseRedirect("/contacts")
    else:
        form = ContactForm(user=request.user)
    return render_to_response("contacts/new.html", {
        'form': form}, 
        RequestContext(request))