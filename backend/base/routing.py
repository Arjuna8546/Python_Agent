
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/agent/(?P<hostname>\w+)/$', consumers.AgentConsumer.as_asgi()),
]
