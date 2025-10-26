"""
Configuraciones de optimización para rendimiento y seguridad
"""

# Configuración de compresión para archivos estáticos
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Configuración de compresión
COMPRESS_ENABLED = True
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.rCSSMinFilter',
]
COMPRESS_JS_FILTERS = [
    'compressor.filters.jsmin.JSMinFilter',
]

# Configuración de caché para templates
TEMPLATES_CACHE = {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'OPTIONS': {
        'loaders': [
            ('django.template.loaders.cached.Loader', [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ]),
        ],
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}

# Configuración de base de datos optimizada
DATABASE_OPTIMIZATIONS = {
    'default': {
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
        'CONN_MAX_AGE': 60,  # Reutilizar conexiones por 60 segundos
    }
}

# Headers de seguridad adicionales
SECURITY_HEADERS = {
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload',
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'X-XSS-Protection': '1; mode=block',
    'Referrer-Policy': 'strict-origin-when-cross-origin',
    'Permissions-Policy': 'geolocation=(), microphone=(), camera=()',
}

# Configuración de rate limiting avanzado
RATE_LIMITING = {
    'LOGIN_ATTEMPTS': {
        'limit': 5,
        'window': 300,  # 5 minutos
        'block_duration': 900,  # 15 minutos
    },
    'REGISTRATION_ATTEMPTS': {
        'limit': 3,
        'window': 3600,  # 1 hora
        'block_duration': 3600,  # 1 hora
    },
    'MEMORY_CREATION': {
        'limit': 10,
        'window': 3600,  # 1 hora
        'block_duration': 1800,  # 30 minutos
    },
}

# Configuración de validación de archivos optimizada
FILE_VALIDATION = {
    'MAX_FILE_SIZE': 5 * 1024 * 1024,  # 5MB
    'ALLOWED_EXTENSIONS': ['jpg', 'jpeg', 'png', 'gif', 'webp'],
    'ALLOWED_MIME_TYPES': [
        'image/jpeg',
        'image/png', 
        'image/gif',
        'image/webp'
    ],
    'MIN_DIMENSIONS': (100, 100),
    'MAX_DIMENSIONS': (4000, 4000),
}

# Configuración de logging optimizada
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        'json': {
            'format': '{"level": "%(levelname)s", "time": "%(asctime)s", "module": "%(module)s", "message": "%(message)s"}',
        },
    },
    'handlers': {
        'file_info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/info.log',
            'maxBytes': 10 * 1024 * 1024,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'file_error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/error.log',
            'maxBytes': 10 * 1024 * 1024,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'security_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/security.log',
            'maxBytes': 10 * 1024 * 1024,  # 10MB
            'backupCount': 10,
            'formatter': 'json',
        },
    },
    'loggers': {
        'django.security': {
            'handlers': ['security_file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'memories.security': {
            'handlers': ['security_file'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}

# Configuración de monitoreo
MONITORING = {
    'HEALTH_CHECK_URL': '/health/',
    'METRICS_URL': '/metrics/',
    'STATUS_CHECKS': [
        'database',
        'cache',
        'storage',
        'memory_usage',
    ],
}

# Configuración de backup automático
BACKUP_CONFIG = {
    'ENABLED': True,
    'SCHEDULE': '0 2 * * *',  # Diario a las 2 AM
    'RETENTION_DAYS': 30,
    'BACKUP_MEDIA': True,
    'BACKUP_DATABASE': True,
    'STORAGE_PATH': 'backups/',
}