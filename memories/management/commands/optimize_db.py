"""
Comando para optimizar la base de datos
"""

from django.core.management.base import BaseCommand
from django.db import connection
from memories.models import Memory
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Optimiza la base de datos y limpia datos innecesarios'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Mostrar qué se haría sin ejecutar cambios',
        )
        parser.add_argument(
            '--vacuum',
            action='store_true',
            help='Ejecutar VACUUM en la base de datos (SQLite)',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🔧 Iniciando optimización de base de datos...')
        )

        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('🔍 Modo dry-run: solo mostrando cambios')
            )

        # Estadísticas iniciales
        self.show_statistics()

        # Limpiar sesiones expiradas
        self.clean_expired_sessions(dry_run)

        # Optimizar imágenes huérfanas
        self.clean_orphaned_images(dry_run)

        # Actualizar estadísticas de la base de datos
        if options['vacuum']:
            self.vacuum_database(dry_run)

        # Estadísticas finales
        self.show_statistics()

        self.stdout.write(
            self.style.SUCCESS('✅ Optimización completada')
        )

    def show_statistics(self):
        """Mostrar estadísticas de la base de datos"""
        total_users = User.objects.count()
        total_memories = Memory.objects.count()
        
        self.stdout.write(f"📊 Estadísticas:")
        self.stdout.write(f"   - Usuarios: {total_users}")
        self.stdout.write(f"   - Recuerdos: {total_memories}")

        # Estadísticas de archivos
        try:
            import os
            media_size = sum(
                os.path.getsize(os.path.join(dirpath, filename))
                for dirpath, dirnames, filenames in os.walk('media')
                for filename in filenames
            )
            self.stdout.write(f"   - Tamaño media: {media_size / (1024*1024):.2f} MB")
        except Exception:
            pass

    def clean_expired_sessions(self, dry_run):
        """Limpiar sesiones expiradas"""
        self.stdout.write("🧹 Limpiando sesiones expiradas...")
        
        if not dry_run:
            from django.core.management import call_command
            call_command('clearsessions')
            self.stdout.write("   ✅ Sesiones expiradas eliminadas")
        else:
            self.stdout.write("   🔍 Se eliminarían las sesiones expiradas")

    def clean_orphaned_images(self, dry_run):
        """Limpiar imágenes huérfanas"""
        self.stdout.write("🖼️  Verificando imágenes huérfanas...")
        
        import os
        from django.conf import settings
        
        media_root = settings.MEDIA_ROOT
        memories_path = os.path.join(media_root, 'memories')
        
        if not os.path.exists(memories_path):
            self.stdout.write("   ℹ️  Directorio de imágenes no existe")
            return

        # Obtener todas las imágenes en uso
        used_images = set()
        for memory in Memory.objects.all():
            if memory.image:
                used_images.add(os.path.basename(memory.image.name))

        # Verificar archivos en el directorio
        orphaned_files = []
        for filename in os.listdir(memories_path):
            if filename not in used_images:
                orphaned_files.append(filename)

        if orphaned_files:
            self.stdout.write(f"   🗑️  Encontradas {len(orphaned_files)} imágenes huérfanas")
            
            if not dry_run:
                for filename in orphaned_files:
                    file_path = os.path.join(memories_path, filename)
                    try:
                        os.remove(file_path)
                        self.stdout.write(f"      - Eliminado: {filename}")
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f"      - Error eliminando {filename}: {e}")
                        )
            else:
                for filename in orphaned_files:
                    self.stdout.write(f"      - Se eliminaría: {filename}")
        else:
            self.stdout.write("   ✅ No se encontraron imágenes huérfanas")

    def vacuum_database(self, dry_run):
        """Ejecutar VACUUM en SQLite"""
        self.stdout.write("🗜️  Optimizando base de datos...")
        
        if not dry_run:
            with connection.cursor() as cursor:
                try:
                    cursor.execute("VACUUM;")
                    self.stdout.write("   ✅ VACUUM ejecutado exitosamente")
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"   ❌ Error ejecutando VACUUM: {e}")
                    )
        else:
            self.stdout.write("   🔍 Se ejecutaría VACUUM en la base de datos")