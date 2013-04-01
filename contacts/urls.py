from django.conf.urls import patterns, url

urlpatterns = patterns('contacts.views',
   url(r'^$', 'contacts', name='contacts'),
   url(r'^add$', 'contacts_add', name='contacts_add'),
)
