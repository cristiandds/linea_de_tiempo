"""
Middleware personalizado para seguridad adicional
"""

import time
from django.http import HttpResponse

# Importación condicional para compatibilidad
try:
    from django.http import HttpResponseTooManyRequests
except ImportError:
    # Fallback para versiones anteriores de Django
    class HttpResponseTooManyRequests(HttpResponse):
        status_code = 429


class SecurityHeadersMiddleware:
    """
    Middleware que añade headers de seguridad adicionales
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Headers de seguridad adicionales
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Content Security Policy básico
        response['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data: blob:; "
            "connect-src 'self';"
        )
        
        return response


class RateLimitMiddleware:
    """
    Middleware básico de rate limiting para formularios
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.attempts = {}  # En producción usar Redis o base de datos

    def __call__(self, request):
        # Rate limiting básico para POST requests
        if request.method == 'POST':
            ip = self.get_client_ip(request)
            current_time = time.time()
            
            # Limpiar intentos antiguos (más de 1 hora)
            self.attempts = {
                k: v for k, v in self.attempts.items() 
                if current_time - v['last_attempt'] < 3600
            }
            
            if ip in self.attempts:
                attempts_data = self.attempts[ip]
                time_diff = current_time - attempts_data['last_attempt']
                
                # Máximo 10 intentos por hora
                if attempts_data['count'] >= 10 and time_diff < 3600:
                    return HttpResponseTooManyRequests(
                        "Demasiados intentos. Intenta de nuevo más tarde."
                    )
                
                # Reset counter si ha pasado más de 1 hora
                if time_diff >= 3600:
                    self.attempts[ip] = {'count': 1, 'last_attempt': current_time}
                else:
                    self.attempts[ip]['count'] += 1
                    self.attempts[ip]['last_attempt'] = current_time
            else:
                self.attempts[ip] = {'count': 1, 'last_attempt': current_time}
        
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        """Obtener IP del cliente"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip