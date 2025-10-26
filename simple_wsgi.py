import sys
import os

# Agregar directorio actual al path
sys.path.insert(0, os.path.dirname(__file__))

# Configurar variables de entorno
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'timeline_love.settings')

# Importar Django
import django
django.setup()

# Crear aplicación WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()