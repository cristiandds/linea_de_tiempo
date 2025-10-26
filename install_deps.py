#!/usr/bin/env python3
"""
Script para instalar dependencias en cPanel
"""

import subprocess
import sys
import os

def install_package(package):
    """Instalar un paquete usando pip"""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        print(f"✅ {package} instalado correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando {package}: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Instalando dependencias para Django...")
    
    # Lista de paquetes necesarios
    packages = [
        'Django==4.2.7',
        'Pillow==10.0.1'
    ]
    
    success_count = 0
    for package in packages:
        if install_package(package):
            success_count += 1
    
    print(f"\n📊 Resultado: {success_count}/{len(packages)} paquetes instalados")
    
    if success_count == len(packages):
        print("🎉 ¡Todas las dependencias instaladas correctamente!")
        
        # Verificar Django
        try:
            import django
            print(f"✅ Django {django.get_version()} disponible")
        except ImportError:
            print("❌ Django no se pudo importar")
            
    else:
        print("⚠️ Algunas dependencias no se pudieron instalar")

if __name__ == '__main__':
    main()