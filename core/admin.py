from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.contrib import messages
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError
from django.contrib.admin import AdminSite
from .models import Categoria, Nutricional, Producto, Rol, Direccion, Usuario, MetodoPago, Venta, DetalleVenta

# Admin personalizado con filtrado por roles
class RoleBasedAdminSite(AdminSite):
    def has_permission(self, request):
        return request.user.is_active and request.user.is_staff

    def index(self, request, extra_context=None):
        # Filtrar modelos según el rol del usuario
        if hasattr(request.user, 'rol') and request.user.rol and request.user.rol.nombre == 'Cliente':
            # Los clientes solo ven su propio perfil
            extra_context = extra_context or {}
            extra_context['show_only_profile'] = True
        return super().index(request, extra_context)

# Instancia personalizada del admin
admin_site = RoleBasedAdminSite(name='role_based_admin')


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')
    search_fields = ('nombre',)
    list_filter = ('nombre',)
    ordering = ('nombre',)
    
    def has_module_permission(self, request):
        # Los clientes no pueden acceder a categorías
        if hasattr(request.user, 'rol') and request.user.rol and request.user.rol.nombre == 'Cliente':
            return False
        return super().has_module_permission(request)

@admin.register(Nutricional)
class NutricionalAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredientes', 'tiempo_preparacion', 'proteinas', 'azucar', 'gluten')
    search_fields = ('ingredientes',)
    list_filter = ('proteinas', 'azucar')
    ordering = ('id',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'marca', 'precio', 'tipo', 'categoria', 'stock_actual', 'stock_status')
    search_fields = ('nombre', 'marca', 'tipo')
    list_filter = ('tipo', 'categoria', 'created_at')
    ordering = ('nombre',)
    list_select_related = ('categoria', 'nutricional')
    actions = ['actualizar_stock', 'marcar_agotado']
    
    def stock_status(self, obj):
        if obj.stock_actual == 0:
            return format_html('<span style="color: red; font-weight: bold;">AGOTADO</span>')
        elif obj.stock_actual < 10:
            return format_html('<span style="color: orange;">BAJO STOCK</span>')
        else:
            return format_html('<span style="color: green;">DISPONIBLE</span>')
    stock_status.short_description = 'Estado Stock'
    
    def actualizar_stock(self, request, queryset):
        updated = 0
        for producto in queryset:
            if producto.stock_actual < 5:
                producto.stock_actual = 50  # Reponer stock
                producto.save()
                updated += 1
        self.message_user(request, f'Stock actualizado para {updated} productos.', messages.SUCCESS)
    actualizar_stock.short_description = "Actualizar stock bajo"
    
    def marcar_agotado(self, request, queryset):
        updated = queryset.update(stock_actual=0)
        self.message_user(request, f'{updated} productos marcados como agotados.', messages.WARNING)
    marcar_agotado.short_description = "Marcar como agotado"
    
    def has_module_permission(self, request):
        # Los clientes no pueden acceder a productos
        if hasattr(request.user, 'rol') and request.user.rol and request.user.rol.nombre == 'Cliente':
            return False
        return super().has_module_permission(request)

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'paterno', 'run', 'rol', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'paterno', 'run')
    list_filter = ('rol', 'is_staff', 'is_active', 'is_superuser')
    ordering = ('first_name',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Información Personal', {'fields': ('paterno', 'materno', 'run', 'fono', 'rol', 'direccion')}),
        ('Auditoría', {'fields': ('created_at', 'updated_at', 'deleted_at')}),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Si el usuario es cliente, solo puede ver su propio perfil
        if hasattr(request.user, 'rol') and request.user.rol and request.user.rol.nombre == 'Cliente':
            return qs.filter(id=request.user.id)
        return qs
    
    def has_add_permission(self, request):
        # Solo admins pueden agregar usuarios
        if hasattr(request.user, 'rol') and request.user.rol and request.user.rol.nombre == 'Cliente':
            return False
        return super().has_add_permission(request)
    
    def has_delete_permission(self, request, obj=None):
        # Solo admins pueden eliminar usuarios
        if hasattr(request.user, 'rol') and request.user.rol and request.user.rol.nombre == 'Cliente':
            return False
        return super().has_delete_permission(request, obj)

@admin.register(MetodoPago)
class MetodoPagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')

# FormSet con validación para DetalleVenta
class DetalleVentaFormSet(BaseInlineFormSet):
    def clean(self):
        if any(self.errors):
            return
        
        total_venta = 0
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                cantidad = form.cleaned_data.get('cantidad', 0)
                precio = form.cleaned_data.get('precio_unitario', 0)
                total_venta += cantidad * precio
                
                # Validación: verificar stock disponible
                producto = form.cleaned_data.get('producto')
                if producto and cantidad > producto.stock_actual:
                    raise ValidationError(f'No hay suficiente stock para {producto.nombre}. Stock disponible: {producto.stock_actual}')
        
        if total_venta <= 0:
            raise ValidationError('La venta debe tener al menos un producto con cantidad mayor a 0.')

# Inline para DetalleVenta
class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1
    fields = ('producto', 'cantidad', 'precio_unitario')
    formset = DetalleVentaFormSet
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('producto')

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'monto_total', 'estado', 'canal_venta', 'fecha', 'monto_coloreado')
    search_fields = ('usuario__first_name', 'usuario__paterno', 'estado')
    list_filter = ('estado', 'canal_venta', 'fecha')
    ordering = ('-fecha',)
    inlines = [DetalleVentaInline]
    list_select_related = ('usuario', 'metodo_pago')
    
    # Acción personalizada
    actions = ['marcar_como_pagado', 'marcar_como_entregado']
    
    def monto_coloreado(self, obj):
        if obj.monto_total > 10000:
            return format_html('<span style="color: green; font-weight: bold;">${}</span>', obj.monto_total)
        elif obj.monto_total > 5000:
            return format_html('<span style="color: orange;">${}</span>', obj.monto_total)
        else:
            return format_html('<span style="color: red;">${}</span>', obj.monto_total)
    monto_coloreado.short_description = 'Monto Total'
    
    def marcar_como_pagado(self, request, queryset):
        updated = queryset.update(estado='Pagado')
        self.message_user(request, f'{updated} ventas marcadas como pagadas.', messages.SUCCESS)
    marcar_como_pagado.short_description = "Marcar como pagado"
    
    def marcar_como_entregado(self, request, queryset):
        updated = queryset.update(estado='Entregado')
        self.message_user(request, f'{updated} ventas marcadas como entregadas.', messages.SUCCESS)
    marcar_como_entregado.short_description = "Marcar como entregado"
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Si el usuario es cliente, solo puede ver sus propias ventas
        if hasattr(request.user, 'rol') and request.user.rol and request.user.rol.nombre == 'Cliente':
            return qs.filter(usuario=request.user)
        return qs
    
    def has_module_permission(self, request):
        # Los clientes pueden ver ventas pero con restricciones
        return True

@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'venta', 'producto', 'cantidad', 'precio_unitario')
    search_fields = ('producto__nombre', 'venta__id')
