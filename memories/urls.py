from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'memories'

urlpatterns = [
    # Página principal
    path('', views.TimelineView.as_view(), name='timeline'),
    path('timeline/', views.TimelineView.as_view(), name='timeline_alt'),  # URL alternativa
    
    # Autenticación
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Gestión de recuerdos
    path('create/', views.CreateMemoryView.as_view(), name='create_memory'),
    path('memory/new/', views.CreateMemoryView.as_view(), name='new_memory'),  # URL alternativa
    path('memory/<int:pk>/', views.MemoryDetailView.as_view(), name='memory_detail'),
    path('memory/<int:pk>/edit/', views.EditMemoryView.as_view(), name='edit_memory'),
    path('memory/<int:pk>/delete/', views.DeleteMemoryView.as_view(), name='delete_memory'),
    
    # URLs de conveniencia
    path('edit/<int:pk>/', views.EditMemoryView.as_view(), name='edit_memory_short'),
    path('delete/<int:pk>/', views.DeleteMemoryView.as_view(), name='delete_memory_short'),
    
    # API endpoints básicos (para futuras mejoras)
    path('api/memories/count/', views.MemoryCountView.as_view(), name='memory_count_api'),
]