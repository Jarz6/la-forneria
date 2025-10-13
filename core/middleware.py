from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseForbidden

class RoleBasedAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Solo aplicar en rutas de admin
        if request.path.startswith('/admin/'):
            if request.user.is_authenticated and hasattr(request.user, 'rol'):
                # Si el usuario tiene rol de Cliente, restringir acceso
                if request.user.rol and request.user.rol.nombre == 'Cliente':
                    # Permitir solo ver sus propios datos
                    if request.path.endswith('/change/') and 'usuario' in request.path:
                        # Verificar que esté editando su propio perfil
                        if str(request.user.id) not in request.path:
                            return HttpResponseForbidden("No tienes permisos para acceder a este recurso.")
                    
                    # Bloquear acceso a ciertos modelos
                    restricted_models = ['venta', 'detalleventa', 'producto', 'categoria', 'nutricional']
                    for model in restricted_models:
                        if f'/{model}/' in request.path and not request.user.is_staff:
                            return HttpResponseForbidden("No tienes permisos para acceder a este módulo.")

        response = self.get_response(request)
        return response
