from django.conf.urls import include, url
from myapp.views import Register

urlpatterns = [
    # Examples:
    # url(r'^$', 'UserStory.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

   # url(r'^message/(?P<user_id>\d+)/$', 'myapp.views.message_send', name='message_send'),
    url(r'^post/$', 'myapp.views.send_message', name='send'),
    url(r'^receive/$', 'myapp.views.receive', name='receive'),
    url(r'^sync/$', 'myapp.views.sync', name='sync'),
    url(r'^register/$', Register.as_view(), name='register'),
    url(r'^logout/$', 'myapp.views.logout', name='logout'),
    url(r'^login/$', 'myapp.views.login', name='login'),
    url(r'^$', 'myapp.views.index', name='home'),
]
