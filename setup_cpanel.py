#!/usr/bin/env python3
"""
Script de configuración para cPanel
Ejecuta este script después de subir los archivos
"""

import os
import sys
import django

# Configurar el entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'timeline_love.settings_cpanel')

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(__file__))

# Configurar Django
django.setup()

def setup_database():
    """Configurar la base de datos"""
    print("🔧 Configurando base de datos...")
    
    # Ejecutar migraciones
    from django.core.management import execute_from_command_line
    
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migraciones ejecutadas correctamente")
    except Exception as e:
        print(f"❌ Error en migraciones: {e}")
        return False
    
    return True

def collect_static():
    """Recolectar archivos estáticos"""
    print("📁 Recolectando archivos estáticos...")
    
    from django.core.management import execute_from_command_line
    
    try:
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        print("✅ Archivos estáticos recolectados")
    except Exception as e:
        print(f"❌ Error recolectando estáticos: {e}")
        return False
    
    return True

def create_superuser():
    """Crear superusuario si no existe"""
    print("👤 Verificando superusuario...")
    
    from django.contrib.auth.models import User
    
    try:
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@softechperu.com',
                password='admin123'  # Cambiar después del deploy
            )
            print("✅ Superusuario creado: admin/admin123")
        else:
            print("✅ Superusuario ya existe")
    except Exception as e:
        print(f"❌ Error creando superusuario: {e}")
        return False
    
    return True

def main():
    """Función principal"""
    print("🚀 Iniciando configuración para cPanel...")
    
    # Ejecutar configuraciones
    if setup_database():
        if collect_static():
            create_superuser()
            print("🎉 ¡Configuración completada!")
            print("📝 Recuerda cambiar la contraseña del admin")
        else:
            print("❌ Error en la configuración")
    else:
        print("❌ Error en la configuración de base de datos")

if __name__ == '__main__':
    main()