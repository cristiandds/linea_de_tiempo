// JavaScript principal para Línea de Tiempo Personal

// Utilidades generales
const TimelineApp = {
    // Inicialización
    init() {
        this.setupImagePreviews();
        this.setupFormValidations();
        this.setupAnimations();
        this.setupMobileMenu();
    },

    // Configurar previews de imágenes
    setupImagePreviews() {
        const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
        
        imageInputs.forEach(input => {
            input.addEventListener('change', function(e) {
                const file = e.target.files[0];
                const previewContainer = document.getElementById('image-preview');
                const previewImg = document.getElementById('preview-img');
                
                if (file && previewContainer && previewImg) {
                    // Validar tipo de archivo
                    if (!file.type.startsWith('image/')) {
                        TimelineApp.showAlert('Por favor selecciona un archivo de imagen válido.', 'error');
                        e.target.value = '';
                        return;
                    }
                    
                    // Validar tamaño (5MB)
                    if (file.size > 5 * 1024 * 1024) {
                        TimelineApp.showAlert('La imagen no puede ser mayor a 5MB.', 'error');
                        e.target.value = '';
                        return;
                    }
                    
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        previewImg.src = e.target.result;
                        previewContainer.classList.remove('hidden');
                        previewContainer.classList.add('fade-in-up');
                    };
                    reader.readAsDataURL(file);
                } else if (previewContainer) {
                    previewContainer.classList.add('hidden');
                }
            });
        });
    },

    // Configurar validaciones de formularios
    setupFormValidations() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            form.addEventListener('submit', function(e) {
                const requiredFields = form.querySelectorAll('[required]');
                let isValid = true;
                
                requiredFields.forEach(field => {
                    if (!field.value.trim()) {
                        isValid = false;
                        field.classList.add('border-red-500');
                        field.classList.remove('border-gray-300');
                    } else {
                        field.classList.remove('border-red-500');
                        field.classList.add('border-gray-300');
                    }
                });
                
                if (!isValid) {
                    e.preventDefault();
                    TimelineApp.showAlert('Por favor completa todos los campos requeridos.', 'error');
                }
            });
        });
    },

    // Configurar animaciones
    setupAnimations() {
        // Animación de entrada para tarjetas
        const cards = document.querySelectorAll('.card-hover');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in-up');
                }
            });
        }, {
            threshold: 0.1
        });
        
        cards.forEach(card => {
            observer.observe(card);
        });
    },

    // Configurar menú móvil
    setupMobileMenu() {
        const mobileMenuButton = document.querySelector('[onclick="toggleMobileMenu()"]');
        const mobileMenu = document.getElementById('mobile-menu');
        
        if (mobileMenuButton && mobileMenu) {
            mobileMenuButton.addEventListener('click', function() {
                mobileMenu.classList.toggle('hidden');
            });
        }
    },

    // Mostrar alertas
    showAlert(message, type = 'info') {
        const alertContainer = document.createElement('div');
        alertContainer.className = `fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg max-w-sm ${
            type === 'error' ? 'bg-red-100 border border-red-400 text-red-700' :
            type === 'success' ? 'bg-green-100 border border-green-400 text-green-700' :
            'bg-blue-100 border border-blue-400 text-blue-700'
        } fade-in-up`;
        
        alertContainer.innerHTML = `
            <div class="flex items-center">
                <div class="flex-shrink-0">
                    ${type === 'error' ? '⚠️' : type === 'success' ? '✅' : 'ℹ️'}
                </div>
                <div class="ml-3">
                    <p class="text-sm font-medium">${message}</p>
                </div>
                <button onclick="this.parentElement.parentElement.remove()" class="ml-auto text-lg leading-none">×</button>
            </div>
        `;
        
        document.body.appendChild(alertContainer);
        
        // Auto-remover después de 5 segundos
        setTimeout(() => {
            if (alertContainer.parentElement) {
                alertContainer.remove();
            }
        }, 5000);
    },

    // Limpiar preview de imagen
    clearImagePreview() {
        const imageInput = document.querySelector('input[type="file"][accept*="image"]');
        const previewContainer = document.getElementById('image-preview');
        
        if (imageInput) imageInput.value = '';
        if (previewContainer) previewContainer.classList.add('hidden');
    }
};

// Funciones globales para compatibilidad
function toggleMobileMenu() {
    const menu = document.getElementById('mobile-menu');
    if (menu) menu.classList.toggle('hidden');
}

function clearImagePreview() {
    TimelineApp.clearImagePreview();
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    TimelineApp.init();
});

// Configurar fecha máxima para campos de fecha
document.addEventListener('DOMContentLoaded', function() {
    const dateInputs = document.querySelectorAll('input[type="date"]');
    const today = new Date().toISOString().split('T')[0];
    
    dateInputs.forEach(input => {
        input.max = today;
    });
});