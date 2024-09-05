from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    path('ws/interview/', consumers.interviewConsumer.as_asgi()),
    # path('ws/interview/', consumers.interviewConsumer.as_asgi()),
]