"""
Configuración de Gunicorn para producción
"""

import multiprocessing
import os

# Configuración del servidor
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100

# Configuración de timeouts
timeout = 30
keepalive = 2
graceful_timeout = 30

# Configuración de logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Configuración de proceso
user = None
group = None
tmp_upload_dir = None
secure_scheme_headers = {
    'X-FORWARDED-PROTOCOL': 'ssl',
    'X-FORWARDED-PROTO': 'https',
    'X-FORWARDED-SSL': 'on'
}

# Configuración de desarrollo vs producción
if os.environ.get('DJANGO_SETTINGS_MODULE') == 'timeline_love.settings_production':
    # Configuración de producción
    workers = multiprocessing.cpu_count() * 2 + 1
    preload_app = True
    max_requests = 1000
else:
    # Configuración de desarrollo
    workers = 1
    reload = True
    preload_app = False