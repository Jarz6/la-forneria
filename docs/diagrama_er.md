# Diagrama Entidad-Relación - La Fornería

## Base de Datos: la_forneria_db

```mermaid
erDiagram
    USUARIO {
        int id PK
        string username UK
        string email UK
        string first_name
        string last_name
        string paterno
        string materno
        string run UK
        string fono
        boolean is_staff
        boolean is_superuser
        boolean is_active
        datetime date_joined
        int rol_id FK
        int direccion_id FK
        datetime created_at
        datetime updated_at
        datetime deleted_at
    }

    ROL {
        int id PK
        string nombre
        text descripcion
        datetime created_at
        datetime updated_at
        datetime deleted_at
    }

    DIRECCION {
        int id PK
        string calle
        string numero
        string comuna
        string region
        datetime created_at
        datetime updated_at
        datetime deleted_at
    }

    CATEGORIA {
        int id PK
        string nombre
        text descripcion
        datetime created_at
        datetime updated_at
        datetime deleted_at
    }

    NUTRICIONAL {
        int id PK
        text ingredientes
        int tiempo_preparacion
        float proteinas
        float azucar
        boolean gluten
        datetime created_at
        datetime updated_at
        datetime deleted_at
    }

    PRODUCTO {
        int id PK
        string nombre
        string marca
        decimal precio
        string tipo
        int stock_actual
        int categoria_id FK
        int nutricional_id FK
        datetime created_at
        datetime updated_at
        datetime deleted_at
    }

    METODO_PAGO {
        int id PK
        string nombre
        datetime created_at
        datetime updated_at
        datetime deleted_at
    }

    VENTA {
        int id PK
        int usuario_id FK
        int metodo_pago_id FK
        decimal monto_total
        string estado
        string canal_venta
        datetime fecha
        datetime created_at
        datetime updated_at
        datetime deleted_at
    }

    DETALLE_VENTA {
        int id PK
        int venta_id FK
        int producto_id FK
        int cantidad
        decimal precio_unitario
        datetime created_at
        datetime updated_at
        datetime deleted_at
    }

    %% Relaciones
    USUARIO ||--o{ ROL : "tiene"
    USUARIO ||--o{ DIRECCION : "vive_en"
    USUARIO ||--o{ VENTA : "realiza"
    
    CATEGORIA ||--o{ PRODUCTO : "contiene"
    NUTRICIONAL ||--o{ PRODUCTO : "describe"
    
    METODO_PAGO ||--o{ VENTA : "utiliza"
    
    VENTA ||--o{ DETALLE_VENTA : "incluye"
    PRODUCTO ||--o{ DETALLE_VENTA : "se_vende_en"
```

## Descripción de las Entidades

### Tablas Maestras (4):
1. **ROL**: Define los roles del sistema (Admin, Cliente)
2. **DIRECCION**: Información de direcciones de usuarios
3. **CATEGORIA**: Categorías de productos (Panadería, Pastelería, Bebidas)
4. **NUTRICIONAL**: Información nutricional de productos

### Tablas Operativas (2):
1. **VENTA**: Registro de ventas realizadas
2. **DETALLE_VENTA**: Detalle de productos en cada venta

### Tabla Principal:
- **USUARIO**: Usuarios del sistema (extiende AbstractUser)
- **PRODUCTO**: Productos de la fornería
- **METODO_PAGO**: Métodos de pago disponibles

## Campos de Auditoría
Todas las tablas incluyen:
- `created_at`: Fecha de creación
- `updated_at`: Fecha de última modificación  
- `deleted_at`: Fecha de eliminación lógica (soft delete)

## Tipos de Datos Utilizados
- `int`: Enteros para IDs y cantidades
- `string`: Cadenas de texto cortas
- `text`: Cadenas de texto largas
- `decimal`: Números decimales para precios
- `boolean`: Valores verdadero/falso
- `datetime`: Fechas y horas
