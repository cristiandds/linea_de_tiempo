from django.contrib import admin
from .models import Memory


@admin.register(Memory)
class MemoryAdmin(admin.ModelAdmin):
    """
    Configuración del admin para el modelo Memory
    """
    list_display = ('title', 'user', 'date', 'created_at')
    list_filter = ('date', 'created_at', 'user')
    search_fields = ('title', 'description')
    date_hierarchy = 'date'
    ordering = ('-date', '-created_at')
    
    fieldsets = (
        ('Información del Recuerdo', {
            'fields': ('title', 'description', 'image', 'date')
        }),
        ('Información del Usuario', {
            'fields': ('user',)
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        """Optimizar consultas con select_related"""
        return super().get_queryset(request).select_related('user')
