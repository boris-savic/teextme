from django.conf.urls import patterns, url

urlpatterns = patterns(
    'messaging.views',
    url(r'^(?P<contact_id>\d+)$',
        'messages_contact',
        name='messages_contact'),
)
