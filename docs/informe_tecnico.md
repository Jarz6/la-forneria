# Informe Técnico - La Fornería
## Aplicación Web Django con Admin Personalizado

### 1. Base de Datos y Conexión

**Base de datos utilizada**: MySQL
**Configuración**: Se utiliza el archivo `.env` para manejar las credenciales de conexión de forma segura.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='3306'),
    }
}
```

**Variables de entorno requeridas**:
- `DB_NAME`: la_forneria_db
- `DB_USER`: root
- `DB_PASSWORD`: password
- `DB_HOST`: localhost
- `DB_PORT`: 3306

### 2. Clasificación de Tablas

#### Tablas Maestras (4):
1. **ROL**: Define roles del sistema (Admin, Cliente)
2. **DIRECCION**: Información de direcciones
3. **CATEGORIA**: Categorías de productos (Panadería, Pastelería, Bebidas)
4. **NUTRICIONAL**: Información nutricional de productos

#### Tablas Operativas (2):
1. **VENTA**: Registro de transacciones de venta
2. **DETALLE_VENTA**: Detalle de productos en cada venta

### 3. Funcionalidades Admin Pro Implementadas

#### 3.1 Inline
**Implementado en**: `VentaAdmin` con `DetalleVentaInline`
- Permite editar los detalles de venta directamente desde la venta
- Formulario tabular con validaciones personalizadas
- Optimización con `select_related` para evitar consultas N+1

```python
class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1
    fields = ('producto', 'cantidad', 'precio_unitario')
    formset = DetalleVentaFormSet
```

#### 3.2 Acción Personalizada
**Implementadas en**: `VentaAdmin` y `ProductoAdmin`

**VentaAdmin**:
- `marcar_como_pagado`: Cambia estado de ventas a "Pagado"
- `marcar_como_entregado`: Cambia estado de ventas a "Entregado"

**ProductoAdmin**:
- `actualizar_stock`: Repone stock para productos con stock bajo
- `marcar_agotado`: Marca productos como agotados

#### 3.3 Validación
**Implementada en**: `DetalleVentaFormSet`

Validaciones incluidas:
- Verificación de stock disponible antes de la venta
- Validación de que la venta tenga al menos un producto
- Validación de cantidades y precios mayores a 0

```python
def clean(self):
    # Verificar stock disponible
    if producto and cantidad > producto.stock_actual:
        raise ValidationError(f'No hay suficiente stock para {producto.nombre}')
```

### 4. Sistema de Seguridad/Roles

#### 4.1 Usuarios Creados
1. **Superusuario**: `admin@forneria.cl` / `admin123`
   - Acceso completo a todos los módulos
   - Permisos de administrador

2. **Usuario Limitado**: `cliente@forneria.cl` / `cliente123`
   - Rol: Cliente
   - Acceso restringido según su rol

#### 4.2 Implementación de Scoping/Rol

**Middleware personalizado**: `RoleBasedAccessMiddleware`
- Intercepta peticiones al admin
- Aplica restricciones según el rol del usuario

**Restricciones para usuarios Cliente**:
- **Modelos bloqueados**: Categoría, Producto, Nutricional
- **Acceso limitado**: Solo puede ver su propio perfil en Usuario
- **Ventas**: Solo puede ver sus propias ventas
- **Sin permisos**: No puede agregar, editar o eliminar en módulos restringidos

**Métodos implementados**:
- `has_module_permission()`: Controla acceso a módulos
- `get_queryset()`: Filtra datos según el usuario
- `has_add_permission()`: Controla permisos de creación
- `has_delete_permission()`: Controla permisos de eliminación

### 5. Modelo Usuario Personalizado

**Extensión**: `AbstractUser`
**Campos adicionales**:
- `paterno`: Apellido paterno
- `materno`: Apellido materno  
- `run`: RUT chileno
- `fono`: Teléfono
- `rol`: Relación con tabla Rol
- `direccion`: Relación con tabla Dirección

**Validación personalizada**:
```python
def clean(self):
    if self.rol and self.rol.nombre == 'Cliente' and self.is_staff:
        raise ValidationError("Los clientes no pueden tener permisos de staff.")
```

### 6. Campos de Auditoría

Todos los modelos incluyen:
- `created_at`: Timestamp de creación automático
- `updated_at`: Timestamp de actualización automático
- `deleted_at`: Timestamp para eliminación lógica (soft delete)

### 7. Comando de Semillas

**Archivo**: `core/management/commands/seed_db.py`

**Datos creados**:
- 2 roles (Admin, Cliente)
- 3 categorías (Panadería, Pastelería, Bebidas)
- 2 direcciones de ejemplo
- 2 perfiles nutricionales
- 3 métodos de pago
- 3 productos de ejemplo
- 2 usuarios (admin y cliente)
- 2 ventas de ejemplo con detalles

### 8. Decisiones de Diseño

#### 8.1 Por qué MySQL
- Mejor rendimiento para aplicaciones web
- Soporte completo para transacciones
- Compatibilidad con Django ORM

#### 8.2 Por qué AbstractUser
- Extiende funcionalidad de autenticación de Django
- Mantiene compatibilidad con admin de Django
- Permite agregar campos personalizados fácilmente

#### 8.3 Por qué Soft Delete
- Preserva integridad referencial
- Permite auditoría completa
- Facilita recuperación de datos

#### 8.4 Por qué Inline en Venta
- Mejora UX al editar ventas y sus detalles
- Reduce navegación entre páginas
- Permite validaciones cruzadas entre venta y detalles

### 9. Instrucciones de Instalación

1. **Crear archivo .env** con las credenciales de base de datos
2. **Instalar dependencias**: `pip install -r requirements.txt`
3. **Ejecutar migraciones**: `python manage.py migrate`
4. **Cargar semillas**: `python manage.py seed_db`
5. **Crear superusuario**: `python manage.py createsuperuser`
6. **Ejecutar servidor**: `python manage.py runserver`

### 10. Credenciales de Acceso

- **Admin**: admin@forneria.cl / admin123
- **Cliente**: cliente@forneria.cl / cliente123

### 11. Evidencias de Funcionamiento

Para demostrar el funcionamiento del sistema:

1. **Login como Admin**: Acceso completo a todos los módulos
2. **Login como Cliente**: 
   - Solo ve módulos permitidos (Usuario, Venta, DetalleVenta)
   - No puede acceder a Categoría, Producto, Nutricional
   - Solo ve sus propias ventas
   - No puede agregar/eliminar usuarios
3. **Inline funcionando**: Editar venta muestra detalles inline
4. **Acciones personalizadas**: Botones para marcar ventas como pagadas/entregadas
5. **Validaciones**: Intentar vender más stock del disponible muestra error
