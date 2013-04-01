from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views


urlpatterns = patterns('',
    url(r'^register/$', 'customregistration.views.register', name='registration_register'),
    url(r'^activate/$', 'customregistration.views.activate', name='registration_activate'),
    url(r'^login/$',
        auth_views.login,
        {'template_name': 'customregistration/login.html'},
        name='auth_login'),
    url(r'^logout/$',
        auth_views.logout,
        {'template_name': 'customregistration/logout.html'},
        name='auth_logout'),
    url(r'^password/change/$',
        auth_views.password_change,
        name='auth_password_change'),
    url(r'^password/change/done/$',
        auth_views.password_change_done,
        name='auth_password_change_done'),
)