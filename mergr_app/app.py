## app.py

import os
from celery import Celery
from django.core.asgi import get_asgi_application
from django.core.wsgi import get_wsgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

# Initialize Django
django.setup()

# Initialize Celery
celery_app = Celery('your_project')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# ASGI application for Channels
asgi_application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                # Define your WebSocket URL routes here
                # Example: websocket_urlpatterns
                []
            )
        )
    ),
})

# WSGI application for Django
wsgi_application = get_wsgi_application()

if __name__ == "__main__":
    # This block is for running the Django application directly
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
