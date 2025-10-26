from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from .models import Memory
from .forms import RegistrationForm, MemoryForm
from .validators import (
    validate_memory_date, 
    validate_memory_title, 
    validate_memory_description,
    validate_username_custom
)
import tempfile
from PIL import Image
import io


class MemoryModelTest(TestCase):
    """
    Tests unitarios para el modelo Memory
    """
    
    def setUp(self):
        """Configuración inicial para los tests"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Crear imagen de prueba
        self.test_image = self.create_test_image()
    
    def create_test_image(self):
        """Crear una imagen de prueba válida"""
        image = Image.new('RGB', (200, 200), color='red')
        image_file = io.BytesIO()
        image.save(image_file, format='JPEG')
        image_file.seek(0)
        return SimpleUploadedFile(
            name='test.jpg',
            content=image_file.getvalue(),
            content_type='image/jpeg'
        )
    
    def test_memory_creation(self):
        """Test de creación básica de recuerdo"""
        memory = Memory(
            user=self.user,
            title='Test Memory',
            description='Esta es una descripción de prueba para el recuerdo',
            image=self.test_image,
            date=date.today()
        )
        # Guardar sin validaciones completas para el test
        memory.save()
        
        self.assertEqual(memory.title, 'Test Memory')
        self.assertEqual(memory.user, self.user)
        self.assertTrue(memory.image)
        self.assertEqual(memory.date, date.today())
        self.assertIsNotNone(memory.created_at)
        self.assertIsNotNone(memory.updated_at)
    
    def test_memory_str_method(self):
        """Test del método __str__ del modelo"""
        memory = Memory(
            user=self.user,
            title='Test Memory',
            description='Descripción de prueba para el test',
            image=self.test_image,
            date=date(2024, 1, 15)
        )
        memory.save()
        
        expected_str = "Test Memory - 2024-01-15"
        self.assertEqual(str(memory), expected_str)
    
    def test_memory_ordering(self):
        """Test del ordenamiento de recuerdos"""
        # Crear recuerdos con diferentes fechas
        # Crear imagen para el primer recuerdo
        image1 = Image.new('RGB', (200, 200), color='red')
        image_file1 = io.BytesIO()
        image1.save(image_file1, format='JPEG')
        image_file1.seek(0)
        test_image1 = SimpleUploadedFile(
            name='old.jpg',
            content=image_file1.getvalue(),
            content_type='image/jpeg'
        )
        
        memory1 = Memory(
            user=self.user,
            title='Recuerdo Antiguo',
            description='Descripción del recuerdo antiguo',
            image=test_image1,
            date=date(2023, 1, 1)
        )
        memory1.save()
        
        # Crear imagen para el segundo recuerdo
        image2 = Image.new('RGB', (200, 200), color='blue')
        image_file2 = io.BytesIO()
        image2.save(image_file2, format='JPEG')
        image_file2.seek(0)
        test_image2 = SimpleUploadedFile(
            name='new.jpg',
            content=image_file2.getvalue(),
            content_type='image/jpeg'
        )
        
        memory2 = Memory(
            user=self.user,
            title='Recuerdo Reciente',
            description='Descripción del recuerdo reciente',
            image=test_image2,
            date=date(2024, 1, 1)
        )
        memory2.save()
        
        memories = Memory.objects.all()
        # Debe estar ordenado por fecha descendente
        self.assertEqual(memories[0], memory2)
        self.assertEqual(memories[1], memory1)
    
    def test_memory_user_relationship(self):
        """Test de la relación con el usuario"""
        memory = Memory(
            user=self.user,
            title='Test Memory',
            description='Descripción de prueba para relación',
            image=self.test_image,
            date=date.today()
        )
        memory.save()
        
        # Verificar relación
        self.assertEqual(memory.user, self.user)
        self.assertIn(memory, self.user.memory_set.all())
    
    def test_memory_date_validation(self):
        """Test de validación de fecha"""
        # Fecha futura debe fallar
        future_date = date.today() + timedelta(days=1)
        
        memory = Memory(
            user=self.user,
            title='Test Memory',
            description='Descripción de prueba para validación',
            image=self.test_image,
            date=future_date
        )
        
        with self.assertRaises(ValidationError):
            memory.full_clean()
    
    def test_memory_title_validation(self):
        """Test de validación de título"""
        # Título muy corto
        memory = Memory(
            user=self.user,
            title='AB',  # Menos de 3 caracteres
            description='Descripción válida para el test',
            image=self.test_image,
            date=date.today()
        )
        
        with self.assertRaises(ValidationError):
            memory.full_clean()
    
    def test_memory_description_validation(self):
        """Test de validación de descripción"""
        # Descripción muy corta
        memory = Memory(
            user=self.user,
            title='Título válido',
            description='Corta',  # Menos de 10 caracteres
            image=self.test_image,
            date=date.today()
        )
        
        with self.assertRaises(ValidationError):
            memory.full_clean()


class ValidatorsTest(TestCase):
    """
    Tests para validadores personalizados
    """
    
    def test_validate_memory_date_valid(self):
        """Test de validación de fecha válida"""
        valid_date = date.today()
        # No debe lanzar excepción
        try:
            validate_memory_date(valid_date)
        except ValidationError:
            self.fail("validate_memory_date lanzó ValidationError con fecha válida")
    
    def test_validate_memory_date_future(self):
        """Test de validación de fecha futura"""
        future_date = date.today() + timedelta(days=1)
        
        with self.assertRaises(ValidationError):
            validate_memory_date(future_date)
    
    def test_validate_memory_date_too_old(self):
        """Test de validación de fecha muy antigua"""
        old_date = date(1900, 1, 1)
        
        with self.assertRaises(ValidationError):
            validate_memory_date(old_date)
    
    def test_validate_memory_title_valid(self):
        """Test de validación de título válido"""
        valid_title = "Mi recuerdo especial"
        
        try:
            validate_memory_title(valid_title)
        except ValidationError:
            self.fail("validate_memory_title lanzó ValidationError con título válido")
    
    def test_validate_memory_title_too_short(self):
        """Test de validación de título muy corto"""
        short_title = "AB"
        
        with self.assertRaises(ValidationError):
            validate_memory_title(short_title)
    
    def test_validate_memory_title_forbidden_chars(self):
        """Test de validación de título con caracteres prohibidos"""
        invalid_title = "Título con <script>"
        
        with self.assertRaises(ValidationError):
            validate_memory_title(invalid_title)
    
    def test_validate_memory_description_valid(self):
        """Test de validación de descripción válida"""
        valid_description = "Esta es una descripción válida para el recuerdo"
        
        try:
            validate_memory_description(valid_description)
        except ValidationError:
            self.fail("validate_memory_description lanzó ValidationError con descripción válida")
    
    def test_validate_memory_description_too_short(self):
        """Test de validación de descripción muy corta"""
        short_description = "Corta"
        
        with self.assertRaises(ValidationError):
            validate_memory_description(short_description)
    
    def test_validate_username_custom_valid(self):
        """Test de validación de nombre de usuario válido"""
        valid_username = "usuario_valido123"
        
        try:
            validate_username_custom(valid_username)
        except ValidationError:
            self.fail("validate_username_custom lanzó ValidationError con username válido")
    
    def test_validate_username_custom_invalid_chars(self):
        """Test de validación de username con caracteres inválidos"""
        invalid_username = "usuario-inválido!"
        
        with self.assertRaises(ValidationError):
            validate_username_custom(invalid_username)
    
    def test_validate_username_custom_starts_with_number(self):
        """Test de validación de username que empieza con número"""
        invalid_username = "123usuario"
        
        with self.assertRaises(ValidationError):
            validate_username_custom(invalid_username)
    
    def test_validate_username_custom_reserved_word(self):
        """Test de validación de username con palabra reservada"""
        reserved_username = "admin"
        
        with self.assertRaises(ValidationError):
            validate_username_custom(reserved_username)


class MemoryFormTest(TestCase):
    """
    Tests para formularios de recuerdos
    """
    
    def setUp(self):
        """Configuración inicial"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.test_image = self.create_test_image()
    
    def create_test_image(self):
        """Crear imagen de prueba"""
        image = Image.new('RGB', (200, 200), color='blue')
        image_file = io.BytesIO()
        image.save(image_file, format='JPEG')
        image_file.seek(0)
        return SimpleUploadedFile(
            name='form.jpg',
            content=image_file.getvalue(),
            content_type='image/jpeg'
        )
    
    def test_memory_form_valid_data(self):
        """Test de formulario con datos válidos"""
        form_data = {
            'title': 'Recuerdo de prueba',
            'description': 'Esta es una descripción válida para el formulario',
            'date': date.today()
        }
        
        form = MemoryForm(data=form_data, files={'image': self.test_image})
        self.assertTrue(form.is_valid())
    
    def test_memory_form_invalid_title(self):
        """Test de formulario con título inválido"""
        form_data = {
            'title': 'AB',  # Muy corto
            'description': 'Descripción válida para el test',
            'date': date.today()
        }
        
        form = MemoryForm(data=form_data, files={'image': self.test_image})
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
    
    def test_memory_form_invalid_description(self):
        """Test de formulario con descripción inválida"""
        form_data = {
            'title': 'Título válido',
            'description': 'Corta',  # Muy corta
            'date': date.today()
        }
        
        form = MemoryForm(data=form_data, files={'image': self.test_image})
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)
    
    def test_memory_form_missing_required_fields(self):
        """Test de formulario con campos requeridos faltantes"""
        form_data = {
            'title': 'Título válido'
            # Faltan description, date e image
        }
        
        form = MemoryForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)
        self.assertIn('date', form.errors)
        self.assertIn('image', form.errors)


class RegistrationFormTest(TestCase):
    """
    Tests para formulario de registro
    """
    
    def test_registration_form_valid_data(self):
        """Test de formulario de registro con datos válidos"""
        form_data = {
            'username': 'nuevo_usuario',
            'email': 'nuevo@example.com',
            'password1': 'contraseña_segura123',
            'password2': 'contraseña_segura123'
        }
        
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_registration_form_invalid_username(self):
        """Test de formulario con username inválido"""
        form_data = {
            'username': '123usuario',  # Empieza con número
            'email': 'test@example.com',
            'password1': 'contraseña_segura123',
            'password2': 'contraseña_segura123'
        }
        
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
    
    def test_registration_form_duplicate_email(self):
        """Test de formulario con email duplicado"""
        # Crear usuario existente
        User.objects.create_user(
            username='existente',
            email='existente@example.com',
            password='password123'
        )
        
        form_data = {
            'username': 'nuevo_usuario',
            'email': 'existente@example.com',  # Email ya existe
            'password1': 'contraseña_segura123',
            'password2': 'contraseña_segura123'
        }
        
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_registration_form_password_mismatch(self):
        """Test de formulario con contraseñas que no coinciden"""
        form_data = {
            'username': 'nuevo_usuario',
            'email': 'nuevo@example.com',
            'password1': 'contraseña_segura123',
            'password2': 'contraseña_diferente456'
        }
        
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)


class MemoryViewsTest(TestCase):
    """
    Tests para vistas de recuerdos
    """
    
    def setUp(self):
        """Configuración inicial"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpass123'
        )
        
        # Crear recuerdo de prueba
        self.memory = Memory(
            user=self.user,
            title='Recuerdo de prueba',
            description='Esta es una descripción de prueba para las vistas',
            image=self.create_test_image(),
            date=date.today()
        )
        self.memory.save()
    
    def create_test_image(self):
        """Crear imagen de prueba"""
        image = Image.new('RGB', (200, 200), color='green')
        image_file = io.BytesIO()
        image.save(image_file, format='JPEG')
        image_file.seek(0)
        return SimpleUploadedFile(
            name='view.jpg',
            content=image_file.getvalue(),
            content_type='image/jpeg'
        )
    
    def test_timeline_view_requires_login(self):
        """Test que la vista timeline requiere login"""
        response = self.client.get(reverse('memories:timeline'))
        self.assertRedirects(response, '/login/?next=/')
    
    def test_timeline_view_authenticated(self):
        """Test de vista timeline con usuario autenticado"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('memories:timeline'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Recuerdo de prueba')
        self.assertContains(response, self.user.username)
    
    def test_timeline_view_only_user_memories(self):
        """Test que timeline solo muestra recuerdos del usuario"""
        # Crear imagen para otro usuario
        other_image = Image.new('RGB', (200, 200), color='yellow')
        other_image_file = io.BytesIO()
        other_image.save(other_image_file, format='JPEG')
        other_image_file.seek(0)
        other_test_image = SimpleUploadedFile(
            name='other.jpg',
            content=other_image_file.getvalue(),
            content_type='image/jpeg'
        )
        
        # Crear recuerdo para otro usuario
        other_memory = Memory(
            user=self.other_user,
            title='Recuerdo de otro usuario',
            description='Este recuerdo no debe aparecer',
            image=other_test_image,
            date=date.today()
        )
        other_memory.save()
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('memories:timeline'))
        
        self.assertContains(response, 'Recuerdo de prueba')
        self.assertNotContains(response, 'Recuerdo de otro usuario')
    
    def test_create_memory_view_requires_login(self):
        """Test que crear recuerdo requiere login"""
        response = self.client.get(reverse('memories:create_memory'))
        self.assertRedirects(response, '/login/?next=/create/')
    
    def test_create_memory_view_authenticated(self):
        """Test de vista crear recuerdo con usuario autenticado"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('memories:create_memory'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Crear Nuevo Recuerdo')
    
    def test_create_memory_post_valid(self):
        """Test de creación de recuerdo con datos válidos"""
        self.client.login(username='testuser', password='testpass123')
        
        form_data = {
            'title': 'Nuevo recuerdo',
            'description': 'Descripción del nuevo recuerdo de prueba',
            'date': date.today(),
            'image': self.create_test_image()
        }
        
        response = self.client.post(reverse('memories:create_memory'), data=form_data)
        
        # Debe redirigir después de crear
        self.assertEqual(response.status_code, 302)
        
        # Verificar que se creó el recuerdo
        new_memory = Memory.objects.filter(title='Nuevo recuerdo').first()
        self.assertIsNotNone(new_memory)
        self.assertEqual(new_memory.user, self.user)
    
    def test_edit_memory_view_owner_only(self):
        """Test que solo el propietario puede editar un recuerdo"""
        # Intentar editar con otro usuario
        self.client.login(username='otheruser', password='otherpass123')
        response = self.client.get(reverse('memories:edit_memory', kwargs={'pk': self.memory.pk}))
        
        self.assertEqual(response.status_code, 404)
    
    def test_edit_memory_view_owner(self):
        """Test de edición de recuerdo por el propietario"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('memories:edit_memory', kwargs={'pk': self.memory.pk}))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Editar Recuerdo')
        self.assertContains(response, self.memory.title)
    
    def test_delete_memory_view_owner_only(self):
        """Test que solo el propietario puede eliminar un recuerdo"""
        # Intentar eliminar con otro usuario
        self.client.login(username='otheruser', password='otherpass123')
        response = self.client.get(reverse('memories:delete_memory', kwargs={'pk': self.memory.pk}))
        
        self.assertEqual(response.status_code, 404)
    
    def test_delete_memory_view_owner(self):
        """Test de eliminación de recuerdo por el propietario"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('memories:delete_memory', kwargs={'pk': self.memory.pk}))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Eliminar Recuerdo')
        self.assertContains(response, self.memory.title)
    
    def test_memory_detail_view_owner_only(self):
        """Test que solo el propietario puede ver detalles de un recuerdo"""
        # Intentar ver con otro usuario
        self.client.login(username='otheruser', password='otherpass123')
        response = self.client.get(reverse('memories:memory_detail', kwargs={'pk': self.memory.pk}))
        
        self.assertEqual(response.status_code, 404)
    
    def test_memory_detail_view_owner(self):
        """Test de vista de detalle por el propietario"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('memories:memory_detail', kwargs={'pk': self.memory.pk}))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.memory.title)
        self.assertContains(response, self.memory.description)


class AuthenticationViewsTest(TestCase):
    """
    Tests para vistas de autenticación
    """
    
    def setUp(self):
        """Configuración inicial"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_login_view_get(self):
        """Test de vista de login GET"""
        response = self.client.get(reverse('memories:login'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bienvenido de vuelta')
    
    def test_login_view_post_valid(self):
        """Test de login con credenciales válidas"""
        form_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        
        response = self.client.post(reverse('memories:login'), data=form_data)
        
        # Debe redirigir después del login
        self.assertEqual(response.status_code, 302)
        
        # Verificar que el usuario está autenticado
        user = response.wsgi_request.user
        self.assertTrue(user.is_authenticated)
    
    def test_login_view_post_invalid(self):
        """Test de login con credenciales inválidas"""
        form_data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        
        response = self.client.post(reverse('memories:login'), data=form_data)
        
        # Debe permanecer en la página de login
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Usuario o contraseña incorrectos')
    
    def test_register_view_get(self):
        """Test de vista de registro GET"""
        response = self.client.get(reverse('memories:register'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Únete a Línea de Tiempo')
    
    def test_register_view_post_valid(self):
        """Test de registro con datos válidos"""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        }
        
        response = self.client.post(reverse('memories:register'), data=form_data)
        
        # Debe redirigir después del registro
        self.assertEqual(response.status_code, 302)
        
        # Verificar que se creó el usuario
        new_user = User.objects.filter(username='newuser').first()
        self.assertIsNotNone(new_user)
        self.assertEqual(new_user.email, 'newuser@example.com')
    
    def test_logout_view(self):
        """Test de vista de logout"""
        # Primero hacer login
        self.client.login(username='testuser', password='testpass123')
        
        # Luego hacer logout
        response = self.client.post(reverse('memories:logout'))
        
        # Debe redirigir
        self.assertEqual(response.status_code, 302)
        
        # Verificar que el usuario ya no está autenticado
        response = self.client.get(reverse('memories:timeline'))
        self.assertRedirects(response, '/login/?next=/')


class IntegrationTest(TestCase):
    """
    Tests de integración que prueban flujos completos de la aplicación
    """
    
    def setUp(self):
        """Configuración inicial"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_basic_functionality(self):
        """
        Test básico de funcionalidad principal
        """
        # 1. Login
        self.client.login(username='testuser', password='testpass123')
        
        # 2. Acceder al timeline
        response = self.client.get(reverse('memories:timeline'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mi Línea de Tiempo')
        
        # 3. Acceder a la página de crear recuerdo
        response = self.client.get(reverse('memories:create_memory'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Crear Nuevo Recuerdo')
        
        # 4. Logout
        response = self.client.post(reverse('memories:logout'))
        self.assertEqual(response.status_code, 302)
        
        # 5. Verificar que no puede acceder sin login
        response = self.client.get(reverse('memories:timeline'))
        self.assertRedirects(response, '/login/?next=/')
    
    def test_authentication_required(self):
        """
        Test que verifica que la autenticación es requerida
        """
        # Intentar acceder sin login
        protected_urls = [
            reverse('memories:timeline'),
            reverse('memories:create_memory'),
        ]
        
        for url in protected_urls:
            response = self.client.get(url)
            self.assertRedirects(response, f'/login/?next={url}')
    
    def test_registration_and_login_flow(self):
        """
        Test del flujo de registro y login
        """
        # 1. Acceder a página de registro
        response = self.client.get(reverse('memories:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Únete a Línea de Tiempo')
        
        # 2. Registrar nuevo usuario
        register_data = {
            'username': 'nuevo_usuario',
            'email': 'nuevo@example.com',
            'password1': 'contraseña_segura123',
            'password2': 'contraseña_segura123'
        }
        
        response = self.client.post(reverse('memories:register'), data=register_data)
        self.assertEqual(response.status_code, 302)  # Redirige después del registro
        
        # 3. Verificar que el usuario se creó
        new_user = User.objects.filter(username='nuevo_usuario').first()
        self.assertIsNotNone(new_user)
        self.assertEqual(new_user.email, 'nuevo@example.com')
        
        # 4. Logout y login manual
        self.client.logout()
        
        login_data = {
            'username': 'nuevo_usuario',
            'password': 'contraseña_segura123'
        }
        
        response = self.client.post(reverse('memories:login'), data=login_data)
        self.assertEqual(response.status_code, 302)  # Redirige después del login
