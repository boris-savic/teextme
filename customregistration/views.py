from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import login

from customregistration.forms import RegistrationForm, ActivationForm


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request, request.POST)
        if form.is_valid():
            new_user = form.save()
            request.session["phone_number"] = new_user.phone_number
            return HttpResponseRedirect("/accounts/activate")
    else:
        form = RegistrationForm(request)
    return render_to_response("customregistration/registration_form.html", {
        'form': form}, 
        RequestContext(request))

def activate(request):
    if request.user.is_active == False:
        if request.method == 'POST':
            form = ActivationForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                return HttpResponseRedirect("/")
        else:
            form = ActivationForm(initial={'phone_number': request.session.get('phone_number', '')})
        return render_to_response("customregistration/activate.html", {
            'form': form}, 
            RequestContext(request))
    else:
        return HttpResponseRedirect("/")


