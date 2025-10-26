#!/usr/bin/env python
"""
Script de despliegue para Línea de Tiempo Personal
"""

import os
import sys
import subprocess
import django
from pathlib import Path

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'timeline_love.settings_production')
django.setup()

def run_command(command, description):
    """Ejecutar comando y mostrar resultado"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado")
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}")
        print(f"   Error: {e.stderr.strip()}")
        return False

def check_requirements():
    """Verificar que todos los requisitos estén instalados"""
    print("🔍 Verificando requisitos...")
    
    required_packages = [
        'django',
        'pillow',
        'gunicorn',
        'whitenoise'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Paquetes faltantes: {', '.join(missing_packages)}")
        print("   Ejecuta: pip install -r requirements.txt")
        return False
    
    print("✅ Todos los requisitos están instalados")
    return True

def create_directories():
    """Crear directorios necesarios"""
    directories = [
        'logs',
        'staticfiles',
        'media/memories'
    ]
    
    for directory in directories:
        path = Path(directory)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            print(f"📁 Directorio creado: {directory}")

def collect_static():
    """Recopilar archivos estáticos"""
    return run_command(
        'python manage.py collectstatic --noinput --clear',
        'Recopilando archivos estáticos'
    )

def run_migrations():
    """Ejecutar migraciones"""
    return run_command(
        'python manage.py migrate',
        'Ejecutando migraciones de base de datos'
    )

def create_superuser():
    """Crear superusuario si no existe"""
    print("\n👤 Verificando superusuario...")
    try:
        from django.contrib.auth.models import User
        if not User.objects.filter(is_superuser=True).exists():
            print("   No se encontró superusuario. Creando uno...")
            username = input("   Nombre de usuario para admin: ")
            email = input("   Email para admin: ")
            
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password='admin123'  # Cambiar después del primer login
            )
            print(f"✅ Superusuario '{username}' creado")
            print("   ⚠️  Contraseña temporal: admin123 (cámbiala después del primer login)")
        else:
            print("✅ Superusuario ya existe")
    except Exception as e:
        print(f"❌ Error creando superusuario: {e}")

def run_tests():
    """Ejecutar tests básicos"""
    return run_command(
        'python manage.py test memories.tests.IntegrationTest.test_basic_functionality --verbosity=0',
        'Ejecutando tests básicos'
    )

def check_deployment():
    """Verificar configuración de despliegue"""
    return run_command(
        'python manage.py check --deploy',
        'Verificando configuración de despliegue'
    )

def main():
    """Función principal de despliegue"""
    print("🚀 Iniciando despliegue de Línea de Tiempo Personal")
    print("=" * 50)
    
    # Verificar requisitos
    if not check_requirements():
        sys.exit(1)
    
    # Crear directorios
    create_directories()
    
    # Ejecutar migraciones
    if not run_migrations():
        print("❌ Fallo en migraciones. Abortando despliegue.")
        sys.exit(1)
    
    # Recopilar archivos estáticos
    if not collect_static():
        print("❌ Fallo recopilando archivos estáticos. Abortando despliegue.")
        sys.exit(1)
    
    # Crear superusuario
    create_superuser()
    
    # Ejecutar tests
    if not run_tests():
        print("⚠️  Tests fallaron, pero continuando con el despliegue...")
    
    # Verificar configuración de despliegue
    check_deployment()
    
    print("\n" + "=" * 50)
    print("🎉 Despliegue completado!")
    print("\n📋 Próximos pasos:")
    print("   1. Configura las variables de entorno (.env)")
    print("   2. Configura el servidor web (Nginx/Apache)")
    print("   3. Inicia el servidor: gunicorn -c gunicorn.conf.py timeline_love.wsgi:application")
    print("   4. Cambia la contraseña del superusuario")
    print("\n🔗 URLs importantes:")
    print("   - Admin: /admin/")
    print("   - Timeline: /")
    print("   - API Count: /api/memories/count/")

if __name__ == '__main__':
    main()