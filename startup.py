#!/usr/bin/env python3
"""
Script de inicialización automática para cPanel
Se ejecuta cuando se inicia la aplicación
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'timeline_love.settings')
django.setup()

def initialize_app():
    """Inicializar la aplicación"""
    try:
        # Ejecutar migraciones si es necesario
        from django.core.management import execute_from_command_line
        from django.db import connection
        
        # Verificar si la base de datos necesita migraciones
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM django_migrations")
        except:
            # Si falla, probablemente necesita migraciones
            print("Ejecutando migraciones...")
            execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
        
        # Recolectar archivos estáticos
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        
        print("Aplicación inicializada correctamente")
        
    except Exception as e:
        print(f"Error en inicialización: {e}")

# Ejecutar inicialización
if __name__ == '__main__':
    initialize_app()