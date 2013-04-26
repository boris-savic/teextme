from django.conf.urls import patterns, url

from rest_framework.urlpatterns import format_suffix_patterns

from contacts.views import ContactList


urlpatterns = patterns('contacts.views',
    url(r'^$', 'contacts', name='contacts'),
    url(r'^add$', 'contacts_add', name='contacts_add'),

    url(r'^api$', ContactList.as_view(), name='contact-list'),

)

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])
