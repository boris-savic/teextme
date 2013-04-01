from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

class RequestTemplateView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(RequestTemplateView, self).get_context_data(**kwargs)
        context['request'] = self.request
        return context

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'teextme.views.home', name='home'),
    # url(r'^teextme/', include('teextme.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
	url(r'^$', RequestTemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^accounts/', include('customregistration.urls')),
    url(r'^messages/', include('messaging.urls')),
    url(r'^contacts/', include('contacts.urls')),
)
