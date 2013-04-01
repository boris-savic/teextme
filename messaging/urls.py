from django.conf.urls import patterns, url

from messaging import views

urlpatterns = patterns('',    
    # ex: /messaging/5/
    url(r'^(?P<contact_id>\d+)/$', views.get_messages, name='get_messages'),
)