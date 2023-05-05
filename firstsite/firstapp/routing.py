from django.conf.urls import url

from . import consumers


websocket_urlpatterns = [
    # url(r'^ws/chat/(?P<f_id>[^/]+)/$', consumers.ChatConsumer),
    url(r'^ws/chat/(?P<f_id>[^/]+)/(?P<u_id>[^/]+)/$', consumers.ChatConsumer),
]
