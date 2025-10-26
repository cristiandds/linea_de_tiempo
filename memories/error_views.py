"""
Vistas personalizadas para manejo de errores
"""
from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponseForbidden


def handler404(request, exception):
    """
    Vista personalizada para error 404 - Página no encontrada
    """
    return render(request, 'errors/404.html', {
        'error_message': 'La página que buscas no existe.',
        'error_code': '404'
    }, status=404)


def handler500(request):
    """
    Vista personalizada para error 500 - Error interno del servidor
    """
    return render(request, 'errors/500.html', {
        'error_message': 'Ha ocurrido un error interno en el servidor.',
        'error_code': '500'
    }, status=500)


def handler403(request, exception):
    """
    Vista personalizada para error 403 - Acceso prohibido
    """
    return render(request, 'errors/403.html', {
        'error_message': 'No tienes permisos para acceder a esta página.',
        'error_code': '403'
    }, status=403)


def handler400(request, exception):
    """
    Vista personalizada para error 400 - Solicitud incorrecta
    """
    return render(request, 'errors/400.html', {
        'error_message': 'La solicitud no es válida.',
        'error_code': '400'
    }, status=400)