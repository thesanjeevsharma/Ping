
from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^register/$', views.register, name='register'),
    url(r'^post/$', views.post, name='post'),
    url(r'^profile/$', views.profile_page, name='profile_page'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^(?P<post_id>[0-9]+)/saved/$', views.saved, name='saved'),
    url(r'^(?P<post_id>[0-9]+)/comment/$', views.comment, name='comment'),
]
