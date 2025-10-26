from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import Http404, JsonResponse
from .models import Memory
from .forms import RegistrationForm, CustomLoginForm, MemoryForm


class CustomLoginView(LoginView):
    """
    Vista de login personalizada con formulario estilizado
    """
    form_class = CustomLoginForm
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        """Mensaje de bienvenida al iniciar sesión"""
        messages.success(self.request, f'¡Bienvenido de vuelta, {form.get_user().username}!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Mensaje de error personalizado"""
        messages.error(self.request, 'Usuario o contraseña incorrectos.')
        return super().form_invalid(form)


class RegisterView(CreateView):
    """
    Vista de registro personalizada con formulario estilizado
    """
    form_class = RegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('memories:timeline')
    
    def form_valid(self, form):
        """Autenticar automáticamente después del registro"""
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, f'¡Bienvenido a Línea de Tiempo, {self.object.username}!')
        return response
    
    def form_invalid(self, form):
        """Mensaje de error en registro"""
        messages.error(self.request, 'Por favor corrige los errores en el formulario.')
        return super().form_invalid(form)


class TimelineView(LoginRequiredMixin, ListView):
    """
    Vista principal que muestra la línea de tiempo de recuerdos del usuario
    """
    model = Memory
    template_name = 'memories/timeline.html'
    context_object_name = 'memories'
    paginate_by = 12  # Paginación para mejor rendimiento
    
    def get_queryset(self):
        """Mostrar solo los recuerdos del usuario autenticado, ordenados cronológicamente"""
        return Memory.objects.filter(user=self.request.user).select_related('user').order_by('-date', '-created_at')
    
    def get_context_data(self, **kwargs):
        """Añadir contexto adicional"""
        context = super().get_context_data(**kwargs)
        context['total_memories'] = self.get_queryset().count()
        return context


class CreateMemoryView(LoginRequiredMixin, CreateView):
    """
    Vista para crear nuevos recuerdos
    """
    model = Memory
    form_class = MemoryForm
    template_name = 'memories/create.html'
    success_url = reverse_lazy('memories:timeline')
    
    def form_valid(self, form):
        """Asociar el recuerdo con el usuario autenticado"""
        form.instance.user = self.request.user
        messages.success(self.request, '¡Recuerdo creado exitosamente!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Mensaje de error en creación"""
        messages.error(self.request, 'Por favor corrige los errores en el formulario.')
        return super().form_invalid(form)


class EditMemoryView(LoginRequiredMixin, UpdateView):
    """
    Vista para editar recuerdos existentes
    """
    model = Memory
    form_class = MemoryForm
    template_name = 'memories/edit.html'
    success_url = reverse_lazy('memories:timeline')
    
    def get_object(self, queryset=None):
        """Verificar que el recuerdo pertenezca al usuario autenticado"""
        obj = get_object_or_404(Memory, pk=self.kwargs['pk'])
        if obj.user != self.request.user:
            raise Http404("No tienes permiso para editar este recuerdo.")
        return obj
    
    def form_valid(self, form):
        """Mensaje de éxito en edición"""
        messages.success(self.request, 'Recuerdo actualizado exitosamente!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Mensaje de error en edición"""
        messages.error(self.request, 'Por favor corrige los errores en el formulario.')
        return super().form_invalid(form)


class DeleteMemoryView(LoginRequiredMixin, DeleteView):
    """
    Vista para eliminar recuerdos con confirmación
    """
    model = Memory
    template_name = 'memories/delete.html'
    success_url = reverse_lazy('memories:timeline')
    
    def get_object(self, queryset=None):
        """Verificar que el recuerdo pertenezca al usuario autenticado"""
        obj = get_object_or_404(Memory, pk=self.kwargs['pk'])
        if obj.user != self.request.user:
            raise Http404("No tienes permiso para eliminar este recuerdo.")
        return obj
    
    def delete(self, request, *args, **kwargs):
        """Mensaje de confirmación y eliminación del archivo de imagen"""
        self.object = self.get_object()
        memory_title = self.object.title
        
        # Eliminar archivo de imagen del sistema de archivos
        if self.object.image:
            try:
                self.object.image.delete(save=False)
            except Exception:
                pass  # Continuar aunque falle la eliminación del archivo
        
        messages.success(request, f'El recuerdo "{memory_title}" ha sido eliminado.')
        return super().delete(request, *args, **kwargs)


class MemoryDetailView(LoginRequiredMixin, DetailView):
    """
    Vista para mostrar detalles de un recuerdo específico
    """
    model = Memory
    template_name = 'memories/detail.html'
    context_object_name = 'memory'
    
    def get_object(self, queryset=None):
        """Verificar que el recuerdo pertenezca al usuario autenticado"""
        obj = get_object_or_404(Memory, pk=self.kwargs['pk'])
        if obj.user != self.request.user:
            raise Http404("No tienes permiso para ver este recuerdo.")
        return obj


class MemoryCountView(LoginRequiredMixin, View):
    """
    Vista API para obtener el conteo de recuerdos del usuario
    """
    
    def get(self, request):
        """Retornar conteo de recuerdos en formato JSON"""
        count = Memory.objects.filter(user=request.user).count()
        return JsonResponse({
            'count': count,
            'user': request.user.username,
            'status': 'success'
        })
