import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from django.urls import path
from base_app.consumers import AppointmentsConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'consultant_app.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket':AuthMiddlewareStack(
        URLRouter([
            path('ws/<int:id>/', AppointmentsConsumer)
        ])
    )
})