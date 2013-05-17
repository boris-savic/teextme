from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from rest_framework.urlpatterns import format_suffix_patterns

from contacts.views import ContactList, ContactDetail
from messaging.views import MessageList, MessageDetail

admin.autodiscover()


class RequestTemplateView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(RequestTemplateView, self).get_context_data(**kwargs)
        context['request'] = self.request
        return context


def auth_login(request):
    return HttpResponseRedirect('/accounts/login/')


urlpatterns = patterns(
    '',
    url(r'^api$', 'teextme.views.api_root'),

    url(r'^api/contacts$', ContactList.as_view(), name='contact-list'),
    url(r'^api/contacts/(?P<pk>\d+)$',
        ContactDetail.as_view(), name='contact-detail'),

    url(r'^api/messages$', MessageList.as_view(), name='message-list'),
    url(r'^api/messages/(?P<pk>\d+)$',
        MessageDetail.as_view(), name='message-detail'),

    url(r'^api/stats$', 'teextme.views.stats', name='stats'),
)

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])

urlpatterns += patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', auth_login, name='index'),
    url(r'^accounts/', include('customregistration.urls')),

    url(r'^app$', login_required(
        RequestTemplateView.as_view(template_name='app.html')), name='app'),
)
