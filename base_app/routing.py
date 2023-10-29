from django.urls import path
from .consumers import AppointmentsConsumer


websocket_urlpatterns = [
    path('ws/book-appointment/', AppointmentsConsumer.as_asgi())
]