from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import FileExtensionValidator
from datetime import date
import uuid
import os
from .validators import (
    ImageValidator, 
    FilenameValidator, 
    validate_memory_date,
    validate_memory_title,
    validate_memory_description
)


def memory_image_upload_path(instance, filename):
    """
    Genera una ruta de subida segura para las imágenes de recuerdos
    """
    # Obtener la extensión del archivo
    ext = os.path.splitext(filename)[1].lower()
    
    # Generar un nombre único y corto
    unique_filename = f"{uuid.uuid4().hex[:12]}{ext}"
    
    # Retornar la ruta completa
    return f'memories/{unique_filename}'


class Memory(models.Model):
    """
    Modelo que representa un recuerdo con foto, título, descripción y fecha.
    Cada recuerdo pertenece a un usuario específico.
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        verbose_name="Usuario",
        help_text="Usuario propietario del recuerdo"
    )
    
    title = models.CharField(
        max_length=200,
        verbose_name="Título",
        help_text="Título del recuerdo (máximo 200 caracteres)",
        validators=[validate_memory_title]
    )
    
    description = models.TextField(
        verbose_name="Descripción",
        help_text="Descripción detallada del recuerdo",
        validators=[validate_memory_description]
    )
    
    image = models.ImageField(
        upload_to=memory_image_upload_path,
        verbose_name="Imagen",
        help_text="Imagen del recuerdo (JPG, PNG, GIF, WEBP - máximo 5MB)",
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp']),
            ImageValidator()
        ]
    )
    
    date = models.DateField(
        verbose_name="Fecha del recuerdo",
        help_text="Fecha en que ocurrió el recuerdo",
        validators=[validate_memory_date]
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de actualización"
    )

    class Meta:
        verbose_name = "Recuerdo"
        verbose_name_plural = "Recuerdos"
        ordering = ['-date', '-created_at']  # Ordenar por fecha del recuerdo (más reciente primero)
        indexes = [
            models.Index(fields=['user', '-date']),  # Índice para consultas por usuario y fecha
        ]

    def __str__(self):
        return f"{self.title} - {self.date}"

    def get_absolute_url(self):
        return reverse('memories:timeline')

    def clean(self):
        """Validaciones personalizadas del modelo"""
        from django.core.exceptions import ValidationError
        
        # Validar que la fecha no sea futura
        if self.date and self.date > date.today():
            raise ValidationError({
                'date': 'La fecha del recuerdo no puede ser futura.'
            })

    def save(self, *args, **kwargs):
        """Sobrescribir save para ejecutar validaciones"""
        self.full_clean()
        super().save(*args, **kwargs)
