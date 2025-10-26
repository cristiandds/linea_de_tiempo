# Línea de Tiempo Personal 💕

Una aplicación web Django moderna y romántica para que parejas puedan subir, visualizar y organizar fotografías de momentos compartidos en una línea de tiempo cronológica privada.

## 🌟 Características

- **Autenticación segura**: Sistema de registro y login con validaciones robustas
- **CRUD completo**: Crear, ver, editar y eliminar recuerdos
- **Diseño romántico**: Interfaz moderna con TailwindCSS y colores rosados
- **Línea de tiempo**: Visualización cronológica de recuerdos con tarjetas visuales
- **Privacidad**: Solo el usuario puede ver y gestionar sus propios recuerdos
- **Responsive**: Diseño adaptado para móviles, tablets y desktop
- **Validaciones**: Validaciones robustas de imágenes, fechas y contenido
- **Seguridad**: Headers de seguridad, CSRF protection, rate limiting

## 🚀 Instalación Rápida

### Requisitos Previos

- Python 3.10+
- pip
- Git

### Instalación en Desarrollo

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd timeline_love
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar base de datos**
   ```bash
   python manage.py migrate
   ```

5. **Crear superusuario**
   ```bash
   python manage.py createsuperuser
   ```

6. **Ejecutar servidor de desarrollo**
   ```bash
   python manage.py runserver
   ```

7. **Acceder a la aplicación**
   - Aplicación: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

## 🏗️ Estructura del Proyecto

```
timeline_love/
├── timeline_love/          # Configuración principal
│   ├── settings.py         # Configuración de desarrollo
│   ├── settings_production.py  # Configuración de producción
│   └── urls.py            # URLs principales
├── memories/              # Aplicación principal
│   ├── models.py          # Modelos de datos
│   ├── views.py           # Lógica de vistas
│   ├── forms.py           # Formularios
│   ├── validators.py      # Validadores personalizados
│   ├── middleware.py      # Middleware de seguridad
│   └── tests.py           # Tests unitarios
├── templates/             # Plantillas HTML
│   ├── base.html          # Template base
│   ├── registration/      # Templates de autenticación
│   ├── memories/          # Templates de recuerdos
│   └── errors/            # Páginas de error personalizadas
├── static/                # Archivos estáticos
│   ├── css/               # Estilos personalizados
│   ├── js/                # JavaScript
│   └── images/            # Imágenes del sitio
├── media/                 # Archivos subidos por usuarios
└── requirements.txt       # Dependencias
```

## 🔧 Configuración de Producción

### 1. Variables de Entorno

Copia `.env.example` a `.env` y configura:

```bash
SECRET_KEY=tu-clave-secreta-muy-larga
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com

# Base de datos PostgreSQL
DB_NAME=timeline_love_prod
DB_USER=timeline_user
DB_PASSWORD=tu-password-seguro
DB_HOST=localhost
DB_PORT=5432

# Email (opcional)
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password
```

### 2. Base de Datos PostgreSQL

```sql
-- Crear base de datos y usuario
CREATE DATABASE timeline_love_prod;
CREATE USER timeline_user WITH PASSWORD 'tu-password-seguro';
GRANT ALL PRIVILEGES ON DATABASE timeline_love_prod TO timeline_user;
```

### 3. Despliegue Automático

```bash
# Usar el script de despliegue
python deploy.py
```

### 4. Servidor Web con Gunicorn

```bash
# Instalar Gunicorn
pip install gunicorn

# Ejecutar servidor
gunicorn -c gunicorn.conf.py timeline_love.wsgi:application
```

### 5. Configuración con Nginx (Opcional)

```nginx
server {
    listen 80;
    server_name tu-dominio.com;
    
    location /static/ {
        alias /ruta/a/timeline_love/staticfiles/;
    }
    
    location /media/ {
        alias /ruta/a/timeline_love/media/;
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🧪 Testing

### Ejecutar Tests

```bash
# Todos los tests
python manage.py test

# Tests específicos
python manage.py test memories.tests.MemoryModelTest
python manage.py test memories.tests.ValidatorsTest
python manage.py test memories.tests.IntegrationTest

# Con cobertura (opcional)
coverage run --source='.' manage.py test
coverage report
```

### Tests Incluidos

- **Tests de Modelos**: Validaciones, relaciones, ordenamiento
- **Tests de Vistas**: CRUD, permisos, autenticación
- **Tests de Formularios**: Validaciones, datos válidos/inválidos
- **Tests de Integración**: Flujos completos de usuario
- **Tests de Validadores**: Validaciones personalizadas

## 🔒 Seguridad

### Características de Seguridad Implementadas

- **CSRF Protection**: Protección contra ataques CSRF
- **XSS Protection**: Headers de seguridad contra XSS
- **Rate Limiting**: Límite de intentos por IP
- **Validación de Archivos**: Validación de tipo, tamaño y contenido de imágenes
- **Control de Acceso**: Solo el propietario puede ver/editar sus recuerdos
- **Sanitización**: Escape de HTML en contenido de usuario
- **Headers de Seguridad**: X-Frame-Options, Content-Security-Policy, etc.

### Configuración de Seguridad en Producción

- SSL/HTTPS obligatorio
- Cookies seguras
- HSTS habilitado
- Validaciones estrictas de archivos
- Logging de seguridad

## 📱 Uso de la Aplicación

### Para Usuarios

1. **Registro**: Crear cuenta con username, email y contraseña
2. **Login**: Iniciar sesión con credenciales
3. **Crear Recuerdo**: Subir foto con título, descripción y fecha
4. **Ver Timeline**: Navegar por recuerdos en orden cronológico
5. **Gestionar**: Editar o eliminar recuerdos propios
6. **Navegación**: Usar breadcrumbs y enlaces para navegar

### Funcionalidades

- **Timeline Principal**: Vista de tarjetas con recuerdos cronológicos
- **Vista Detallada**: Ver recuerdo completo con metadatos
- **Formularios**: Crear y editar recuerdos con validación
- **Confirmación**: Eliminación segura con confirmación
- **Responsive**: Funciona en móviles y tablets

## 🛠️ Desarrollo

### Configuración de Desarrollo

```bash
# Instalar dependencias de desarrollo
pip install coverage django-debug-toolbar

# Configurar settings de desarrollo
export DJANGO_SETTINGS_MODULE=timeline_love.settings

# Ejecutar con debug
python manage.py runserver --settings=timeline_love.settings
```

### Estructura de Código

- **Modelos**: `memories/models.py` - Modelo Memory con validaciones
- **Vistas**: `memories/views.py` - Vistas basadas en clases
- **Formularios**: `memories/forms.py` - Formularios con TailwindCSS
- **Validadores**: `memories/validators.py` - Validaciones personalizadas
- **Templates**: `templates/` - HTML con TailwindCSS
- **Estáticos**: `static/` - CSS y JS personalizados

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📞 Soporte

Para soporte o preguntas:

- Crear un issue en el repositorio
- Revisar la documentación
- Ejecutar tests para verificar funcionamiento

---

**Línea de Tiempo Personal** - Creado con ❤️ para preservar tus recuerdos más preciados.