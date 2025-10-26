from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Memory
from .validators import validate_username_custom


class RegistrationForm(UserCreationForm):
    """
    Formulario de registro personalizado con campo email y estilos TailwindCSS
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent transition-colors',
            'placeholder': 'tu@email.com'
        })
    )
    
    username = forms.CharField(
        validators=[validate_username_custom],
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent transition-colors',
            'placeholder': 'Nombre de usuario'
        })
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent transition-colors',
            'placeholder': 'Contraseña'
        })
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent transition-colors',
            'placeholder': 'Confirmar contraseña'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        """Validar que el email no esté ya registrado"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este email ya está registrado.')
        return email

    def save(self, commit=True):
        """Guardar usuario con email"""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CustomLoginForm(AuthenticationForm):
    """
    Formulario de login personalizado con estilos TailwindCSS
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent transition-colors',
            'placeholder': 'Nombre de usuario'
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent transition-colors',
            'placeholder': 'Contraseña'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar mensajes de error
        self.error_messages['invalid_login'] = 'Usuario o contraseña incorrectos.'
        self.error_messages['inactive'] = 'Esta cuenta está inactiva.'


class MemoryForm(forms.ModelForm):
    """
    Formulario para crear y editar recuerdos con estilos TailwindCSS
    """
    class Meta:
        model = Memory
        fields = ('title', 'description', 'image', 'date')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent transition-colors',
                'placeholder': 'Título del recuerdo'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent transition-colors resize-none',
                'rows': 4,
                'placeholder': 'Describe este hermoso recuerdo...'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent transition-colors file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-pink-50 file:text-pink-700 hover:file:bg-pink-100',
                'accept': 'image/*'
            }),
            'date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent transition-colors',
                'type': 'date'
            })
        }
        labels = {
            'title': 'Título',
            'description': 'Descripción',
            'image': 'Imagen',
            'date': 'Fecha del recuerdo'
        }
        help_texts = {
            'title': 'Un título memorable para tu recuerdo',
            'description': 'Cuenta la historia detrás de esta foto',
            'image': 'Sube una imagen (JPG, PNG, GIF - máximo 5MB)',
            'date': 'Fecha en que ocurrió este recuerdo'
        }

    def clean_image(self):
        """Validar imagen con validaciones adicionales"""
        image = self.cleaned_data.get('image')
        if image:
            # Validar tamaño máximo de 5MB
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError('La imagen no puede ser mayor a 5MB.')
            
            # Validar tipo MIME básico
            if not image.content_type.startswith('image/'):
                raise forms.ValidationError('El archivo debe ser una imagen válida.')
            
            # Validar extensión del nombre de archivo
            import os
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
            file_ext = os.path.splitext(image.name)[1].lower()
            if file_ext not in allowed_extensions:
                raise forms.ValidationError(
                    f'Extensión no permitida: {file_ext}. '
                    f'Extensiones permitidas: {", ".join(allowed_extensions)}'
                )
        return image
    
    def clean_title(self):
        """Validar título con sanitización"""
        title = self.cleaned_data.get('title')
        if title:
            # Sanitizar HTML básico
            import html
            title = html.escape(title.strip())
            
            # Validar longitud después de sanitización
            if len(title) < 3:
                raise forms.ValidationError('El título debe tener al menos 3 caracteres.')
        return title
    
    def clean_description(self):
        """Validar descripción con sanitización"""
        description = self.cleaned_data.get('description')
        if description:
            # Sanitizar HTML básico
            import html
            description = html.escape(description.strip())
            
            # Validar longitud después de sanitización
            if len(description) < 10:
                raise forms.ValidationError('La descripción debe tener al menos 10 caracteres.')
        return description

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer todos los campos requeridos excepto imagen en edición
        for field_name, field in self.fields.items():
            if field_name == 'image' and self.instance.pk:
                # En edición, la imagen no es requerida (mantener la actual)
                field.required = False
            else:
                field.required = True