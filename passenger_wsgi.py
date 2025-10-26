import sys
import os

# Agregar el directorio del proyecto al path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Configurar Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'timeline_love.settings_cpanel')

try:
    # Importar Django
    import django
    django.setup()
    
    # Importar la aplicación WSGI
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    
except Exception as e:
    # Si hay error, crear una aplicación simple que muestre el error
    def application(environ, start_response):
        status = '500 Internal Server Error'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return [f'Error: {str(e)}'.encode('utf-8')]