from django.urls import path
from .consumers import AppointmentsConsumer, PrivateMessagingConsumer


websocket_urlpatterns = [
    path('ws/book-appointment/', AppointmentsConsumer.as_asgi()),
    path('ws/private-messaging/', PrivateMessagingConsumer.as_asgi())
]