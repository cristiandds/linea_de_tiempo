def application(environ, start_response):
    """Aplicación WSGI mínima para probar"""
    status = '200 OK'
    headers = [('Content-type', 'text/html')]
    start_response(status, headers)
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test cPanel</title>
    </head>
    <body>
        <h1>¡cPanel funciona!</h1>
        <p>Python está funcionando correctamente.</p>
        <p>Ahora podemos configurar Django.</p>
    </body>
    </html>
    """
    
    return [html.encode('utf-8')]