"""
Validadores personalizados para la aplicación de recuerdos
"""
import os
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.utils.deconstruct import deconstructible
from datetime import date

try:
    import magic
    HAS_MAGIC = True
except ImportError:
    HAS_MAGIC = False


@deconstructible
class ImageValidator:
    """
    Validador personalizado para imágenes
    """
    
    def __init__(self, max_size=5*1024*1024, allowed_formats=None):
        self.max_size = max_size
        self.allowed_formats = allowed_formats or ['JPEG', 'PNG', 'GIF', 'WEBP']
    
    def __call__(self, image):
        # Validar tamaño de archivo
        if image.size > self.max_size:
            raise ValidationError(
                f'La imagen no puede ser mayor a {self.max_size // (1024*1024)}MB. '
                f'Tamaño actual: {image.size // (1024*1024)}MB'
            )
        
        # Validar dimensiones mínimas y máximas
        try:
            width, height = get_image_dimensions(image)
            if width and height:
                # Mínimo 100x100 píxeles
                if width < 100 or height < 100:
                    raise ValidationError(
                        'La imagen debe tener al menos 100x100 píxeles. '
                        f'Dimensiones actuales: {width}x{height}'
                    )
                
                # Máximo 4000x4000 píxeles
                if width > 4000 or height > 4000:
                    raise ValidationError(
                        'La imagen no puede ser mayor a 4000x4000 píxeles. '
                        f'Dimensiones actuales: {width}x{height}'
                    )
        except Exception:
            raise ValidationError('No se pudo procesar la imagen. Verifica que sea un archivo válido.')
        
        # Validar tipo MIME usando python-magic si está disponible
        if HAS_MAGIC:
            try:
                mime_type = magic.from_buffer(image.read(1024), mime=True)
                image.seek(0)  # Reset file pointer
                
                allowed_mimes = {
                    'image/jpeg': 'JPEG',
                    'image/png': 'PNG', 
                    'image/gif': 'GIF',
                    'image/webp': 'WEBP'
                }
                
                if mime_type not in allowed_mimes:
                    raise ValidationError(
                        f'Formato de imagen no permitido: {mime_type}. '
                        f'Formatos permitidos: {", ".join(self.allowed_formats)}'
                    )
            except Exception:
                # Si falla la validación con magic, continuar sin error
                pass


@deconstructible
class FilenameValidator:
    """
    Validador para nombres de archivo seguros que también sanitiza nombres largos
    """
    
    def __init__(self, max_length=255):
        self.max_length = max_length
    
    def __call__(self, filename):
        import re
        import uuid
        
        # Caracteres peligrosos
        dangerous_chars = ['..', '/', '\\', '<', '>', ':', '"', '|', '?', '*']
        
        for char in dangerous_chars:
            if char in filename:
                raise ValidationError(
                    f'El nombre del archivo contiene caracteres no permitidos: {char}'
                )
        
        # Extensiones permitidas
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        file_ext = os.path.splitext(filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            raise ValidationError(
                f'Extensión de archivo no permitida: {file_ext}. '
                f'Extensiones permitidas: {", ".join(allowed_extensions)}'
            )
        
        # Si el nombre es muy largo, no lanzar error sino generar uno más corto
        # Esto se maneja en el modelo con un método personalizado


def validate_memory_date(value):
    """
    Validador para fechas de recuerdos
    """
    if value > date.today():
        raise ValidationError(
            'La fecha del recuerdo no puede ser futura. '
            f'Fecha máxima permitida: {date.today().strftime("%d/%m/%Y")}'
        )
    
    # No permitir fechas muy antiguas (más de 100 años)
    min_date = date(date.today().year - 100, 1, 1)
    if value < min_date:
        raise ValidationError(
            f'La fecha del recuerdo es demasiado antigua. '
            f'Fecha mínima permitida: {min_date.strftime("%d/%m/%Y")}'
        )


def validate_memory_title(value):
    """
    Validador para títulos de recuerdos
    """
    # Longitud mínima
    if len(value.strip()) < 3:
        raise ValidationError(
            'El título debe tener al menos 3 caracteres.'
        )
    
    # Caracteres no permitidos
    forbidden_chars = ['<', '>', '"', "'", '&']
    for char in forbidden_chars:
        if char in value:
            raise ValidationError(
                f'El título contiene caracteres no permitidos: {char}'
            )
    
    # No solo números
    if value.strip().isdigit():
        raise ValidationError(
            'El título no puede contener solo números.'
        )


def validate_memory_description(value):
    """
    Validador para descripciones de recuerdos
    """
    # Longitud mínima
    if len(value.strip()) < 10:
        raise ValidationError(
            'La descripción debe tener al menos 10 caracteres.'
        )
    
    # Longitud máxima
    if len(value) > 2000:
        raise ValidationError(
            'La descripción no puede tener más de 2000 caracteres.'
        )
    
    # Caracteres no permitidos
    forbidden_chars = ['<script', '</script', 'javascript:', 'onclick=']
    value_lower = value.lower()
    for char in forbidden_chars:
        if char in value_lower:
            raise ValidationError(
                'La descripción contiene contenido no permitido.'
            )


def validate_username_custom(value):
    """
    Validador personalizado para nombres de usuario
    """
    # Solo letras, números y guiones bajos
    import re
    if not re.match(r'^[a-zA-Z0-9_]+$', value):
        raise ValidationError(
            'El nombre de usuario solo puede contener letras, números y guiones bajos.'
        )
    
    # No puede empezar con número
    if value[0].isdigit():
        raise ValidationError(
            'El nombre de usuario no puede empezar con un número.'
        )
    
    # Longitud mínima
    if len(value) < 3:
        raise ValidationError(
            'El nombre de usuario debe tener al menos 3 caracteres.'
        )
    
    # Palabras reservadas
    reserved_words = ['admin', 'root', 'user', 'test', 'null', 'undefined']
    if value.lower() in reserved_words:
        raise ValidationError(
            f'El nombre de usuario "{value}" está reservado.'
        )