from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
from django.contrib.auth.decorators import login_required

admin.autodiscover()

class RequestTemplateView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(RequestTemplateView, self).get_context_data(**kwargs)
        context['request'] = self.request
        return context

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
	url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^accounts/', include('customregistration.urls')),
    url(r'^messages/', include('messaging.urls')),
    url(r'^contacts/', include('contacts.urls')),
    
    url(r'^app$', login_required(RequestTemplateView.as_view(template_name='app.html')), name='app'),
)
