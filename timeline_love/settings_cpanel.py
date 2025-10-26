"""
Configuración específica para cPanel
"""

from .settings import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: define the correct hosts in production.
ALLOWED_HOSTS = [
    'softechperu.com',
    'www.softechperu.com',
    'localhost',
    '127.0.0.1',
]

# Base de datos para cPanel (SQLite por simplicidad)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db_production.sqlite3',
    }
}

# Configuración de archivos estáticos para cPanel
STATIC_URL = '/timeline/static/'
STATIC_ROOT = BASE_DIR / 'static_collected'

# Configuración de archivos media
MEDIA_URL = '/timeline/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Configuración de seguridad básica
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Configuración de sesiones
SESSION_COOKIE_SECURE = False  # cPanel puede no tener HTTPS
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 3600 * 24 * 7  # 1 semana

# CSRF protection
CSRF_COOKIE_SECURE = False  # cPanel puede no tener HTTPS
CSRF_COOKIE_HTTPONLY = True

# Configuración de logging simplificada
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'django_errors.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# Desactivar algunas características que pueden causar problemas en cPanel
USE_TZ = True
TIME_ZONE = 'America/Lima'  # Ajusta según tu zona horaria

# Configuración de email (opcional)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'