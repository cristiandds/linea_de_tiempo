#!/usr/bin/env python3
"""
Script de diagnóstico para cPanel
"""

import sys
import os

def test_environment():
    """Probar el entorno"""
    print("=== DIAGNÓSTICO DE ENTORNO ===")
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Script directory: {os.path.dirname(__file__)}")
    
    print("\n=== ARCHIVOS EN DIRECTORIO ===")
    try:
        files = os.listdir('.')
        for f in files:
            print(f"- {f}")
    except Exception as e:
        print(f"Error listando archivos: {e}")
    
    print("\n=== PROBANDO DJANGO ===")
    try:
        # Configurar Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'timeline_love.settings_cpanel')
        
        import django
        print(f"Django version: {django.get_version()}")
        
        django.setup()
        print("✅ Django configurado correctamente")
        
        # Probar importar settings
        from django.conf import settings
        print(f"✅ Settings cargados: {settings.DEBUG}")
        
        # Probar WSGI
        from django.core.wsgi import get_wsgi_application
        app = get_wsgi_application()
        print("✅ WSGI application creada correctamente")
        
    except Exception as e:
        print(f"❌ Error con Django: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_environment()