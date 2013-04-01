from django.conf.urls import patterns, url

from contacts import views

urlpatterns = patterns('',
   url(r'^$', views.index, name='index'),
   url(r'^add/', views.add_contact, name='add_contact'),
   #url(r'^contacts/add$', 'contacts.views.add_contact', name='add_contact'),
)
