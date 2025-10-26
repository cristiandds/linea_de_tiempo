#!/usr/bin/python3.10
"""
Archivo WSGI para cPanel/Passenger
"""

import sys
import os

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(__file__))

# Configurar Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'timeline_love.settings_cpanel')

# Importar la aplicación WSGI de Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()