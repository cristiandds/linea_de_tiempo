"""
Comando para verificar la salud del sistema
"""

from django.core.management.base import BaseCommand
from django.db import connection
from django.core.cache import cache
from django.conf import settings
import os
import psutil
import time


class Command(BaseCommand):
    help = 'Verifica la salud del sistema y sus componentes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--format',
            choices=['text', 'json'],
            default='text',
            help='Formato de salida (text o json)',
        )

    def handle(self, *args, **options):
        format_type = options['format']
        
        if format_type == 'text':
            self.stdout.write(
                self.style.SUCCESS('🏥 Verificación de salud del sistema')
            )
            self.stdout.write('=' * 50)

        checks = [
            ('Base de Datos', self.check_database),
            ('Cache', self.check_cache),
            ('Archivos Media', self.check_media_storage),
            ('Memoria del Sistema', self.check_system_memory),
            ('Espacio en Disco', self.check_disk_space),
            ('Configuración', self.check_configuration),
        ]

        results = {}
        all_healthy = True

        for check_name, check_function in checks:
            try:
                result = check_function()
                results[check_name] = result
                
                if format_type == 'text':
                    status_icon = '✅' if result['healthy'] else '❌'
                    self.stdout.write(f"{status_icon} {check_name}: {result['message']}")
                    
                    if 'details' in result:
                        for detail in result['details']:
                            self.stdout.write(f"   - {detail}")
                
                if not result['healthy']:
                    all_healthy = False
                    
            except Exception as e:
                results[check_name] = {
                    'healthy': False,
                    'message': f'Error en verificación: {str(e)}'
                }
                all_healthy = False
                
                if format_type == 'text':
                    self.stdout.write(
                        self.style.ERROR(f"❌ {check_name}: Error - {str(e)}")
                    )

        if format_type == 'json':
            import json
            output = {
                'overall_health': all_healthy,
                'timestamp': time.time(),
                'checks': results
            }
            self.stdout.write(json.dumps(output, indent=2))
        else:
            self.stdout.write('=' * 50)
            overall_status = '🟢 SALUDABLE' if all_healthy else '🔴 PROBLEMAS DETECTADOS'
            self.stdout.write(f"Estado general: {overall_status}")

    def check_database(self):
        """Verificar conexión a la base de datos"""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                
            if result and result[0] == 1:
                return {
                    'healthy': True,
                    'message': 'Conexión exitosa',
                    'details': [f'Motor: {connection.vendor}']
                }
            else:
                return {
                    'healthy': False,
                    'message': 'Respuesta inesperada de la base de datos'
                }
        except Exception as e:
            return {
                'healthy': False,
                'message': f'Error de conexión: {str(e)}'
            }

    def check_cache(self):
        """Verificar sistema de cache"""
        try:
            test_key = 'health_check_test'
            test_value = 'test_value'
            
            cache.set(test_key, test_value, 30)
            retrieved_value = cache.get(test_key)
            cache.delete(test_key)
            
            if retrieved_value == test_value:
                return {
                    'healthy': True,
                    'message': 'Cache funcionando correctamente'
                }
            else:
                return {
                    'healthy': False,
                    'message': 'Cache no está funcionando correctamente'
                }
        except Exception as e:
            return {
                'healthy': False,
                'message': f'Error en cache: {str(e)}'
            }

    def check_media_storage(self):
        """Verificar almacenamiento de archivos media"""
        try:
            media_root = settings.MEDIA_ROOT
            
            if not os.path.exists(media_root):
                return {
                    'healthy': False,
                    'message': 'Directorio media no existe'
                }
            
            if not os.access(media_root, os.W_OK):
                return {
                    'healthy': False,
                    'message': 'No hay permisos de escritura en directorio media'
                }
            
            # Verificar espacio disponible
            stat = os.statvfs(media_root)
            free_space = stat.f_bavail * stat.f_frsize
            free_space_mb = free_space / (1024 * 1024)
            
            if free_space_mb < 100:  # Menos de 100MB
                return {
                    'healthy': False,
                    'message': f'Poco espacio disponible: {free_space_mb:.1f}MB'
                }
            
            return {
                'healthy': True,
                'message': 'Almacenamiento media OK',
                'details': [f'Espacio libre: {free_space_mb:.1f}MB']
            }
            
        except Exception as e:
            return {
                'healthy': False,
                'message': f'Error verificando media: {str(e)}'
            }

    def check_system_memory(self):
        """Verificar memoria del sistema"""
        try:
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            if memory_percent > 90:
                return {
                    'healthy': False,
                    'message': f'Memoria alta: {memory_percent:.1f}%'
                }
            elif memory_percent > 80:
                return {
                    'healthy': True,
                    'message': f'Memoria moderada: {memory_percent:.1f}%'
                }
            else:
                return {
                    'healthy': True,
                    'message': f'Memoria OK: {memory_percent:.1f}%',
                    'details': [
                        f'Total: {memory.total / (1024**3):.1f}GB',
                        f'Disponible: {memory.available / (1024**3):.1f}GB'
                    ]
                }
        except Exception as e:
            return {
                'healthy': False,
                'message': f'Error verificando memoria: {str(e)}'
            }

    def check_disk_space(self):
        """Verificar espacio en disco"""
        try:
            disk_usage = psutil.disk_usage('.')
            percent_used = (disk_usage.used / disk_usage.total) * 100
            free_gb = disk_usage.free / (1024**3)
            
            if percent_used > 95:
                return {
                    'healthy': False,
                    'message': f'Disco casi lleno: {percent_used:.1f}%'
                }
            elif percent_used > 85:
                return {
                    'healthy': True,
                    'message': f'Espacio en disco bajo: {percent_used:.1f}%'
                }
            else:
                return {
                    'healthy': True,
                    'message': f'Espacio en disco OK: {percent_used:.1f}%',
                    'details': [f'Espacio libre: {free_gb:.1f}GB']
                }
        except Exception as e:
            return {
                'healthy': False,
                'message': f'Error verificando disco: {str(e)}'
            }

    def check_configuration(self):
        """Verificar configuración crítica"""
        issues = []
        
        # Verificar DEBUG en producción
        if settings.DEBUG:
            issues.append('DEBUG está habilitado (no recomendado en producción)')
        
        # Verificar SECRET_KEY
        if 'django-insecure' in settings.SECRET_KEY:
            issues.append('SECRET_KEY usa valor por defecto inseguro')
        
        # Verificar ALLOWED_HOSTS
        if not settings.ALLOWED_HOSTS or settings.ALLOWED_HOSTS == ['*']:
            issues.append('ALLOWED_HOSTS no está configurado correctamente')
        
        if issues:
            return {
                'healthy': False,
                'message': 'Problemas de configuración detectados',
                'details': issues
            }
        else:
            return {
                'healthy': True,
                'message': 'Configuración OK'
            }