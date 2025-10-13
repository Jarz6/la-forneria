# La Fornería - Sistema de Gestión

Aplicación web Django para la gestión de una fornería, implementando Django Admin personalizado con sistema de roles y seguridad.

## Características Implementadas

### ✅ Conexión a Base de Datos
- Configuración con SQLite (fácil de configurar en laboratorio)
- Migraciones aplicadas correctamente
- Modelo Usuario personalizado extendiendo `AbstractUser`

### ✅ Django Admin Básico
- **4 Tablas Maestras**: Rol, Dirección, Categoría, Nutricional
- **2 Tablas Operativas**: Venta, DetalleVenta
- Configuración completa: `list_display`, `search_fields`, `list_filter`, `ordering`, `list_select_related`

### ✅ Django Admin Pro
- **Inline**: DetalleVenta inline en Venta
- **Acción Personalizada**: Marcar ventas como pagadas/entregadas, actualizar stock
- **Validación**: FormSet con validación de stock y cantidades

### ✅ Sistema de Seguridad/Roles
- **2 Usuarios**: Admin (acceso completo) y Cliente (acceso limitado)
- **Scoping por rol**: Clientes solo ven sus propios datos
- **Restricciones**: Modelos bloqueados para usuarios Cliente
- **Middleware personalizado**: Control de acceso basado en roles

### ✅ Campos de Auditoría
- `created_at`, `updated_at`, `deleted_at` en todos los modelos
- Soft delete implementado

## Instalación

### 1. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 2. Ejecutar Migraciones
```bash
python manage.py migrate
```

### 3. Cargar Datos de Prueba
```bash
python manage.py seed_db
```

### 4. Ejecutar Servidor
```bash
python manage.py runserver
```

## Credenciales de Acceso

### Admin (Acceso Completo)
- **Email**: admin@forneria.cl
- **Password**: admin123

### Cliente (Acceso Limitado)
- **Email**: cliente@forneria.cl
- **Password**: cliente123

## Estructura de la Base de Datos

### Tablas Maestras
- **ROL**: Roles del sistema (Admin, Cliente)
- **DIRECCION**: Direcciones de usuarios
- **CATEGORIA**: Categorías de productos
- **NUTRICIONAL**: Información nutricional

### Tablas Operativas
- **VENTA**: Registro de ventas
- **DETALLE_VENTA**: Detalles de productos en ventas

### Tablas Principales
- **USUARIO**: Usuarios del sistema (personalizado)
- **PRODUCTO**: Productos de la fornería
- **METODO_PAGO**: Métodos de pago

## Funcionalidades del Admin

### Para Administradores
- Acceso completo a todos los módulos
- Gestión de usuarios, productos, ventas
- Acciones personalizadas para gestión de stock
- Inline para edición de detalles de venta

### Para Clientes
- Solo acceso a su perfil de usuario
- Visualización de sus propias ventas
- Sin acceso a gestión de productos o categorías
- Restricciones de permisos implementadas

## Validaciones Implementadas

- **Stock**: No se puede vender más productos de los disponibles
- **Precios**: Deben ser mayores a 0
- **Cantidades**: Deben ser positivas
- **Roles**: Clientes no pueden tener permisos de staff

## Documentación

- `docs/diagrama_er.md`: Diagrama entidad-relación
- `docs/informe_tecnico.md`: Documentación técnica completa

## Tecnologías Utilizadas

- **Django 5.2.7**: Framework web
- **SQLite**: Base de datos (fácil configuración)
- **Django Admin**: Interfaz de administración personalizada
