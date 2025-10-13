from django.core.management.base import BaseCommand
from core.models import Categoria, Rol, Usuario, Direccion, Producto, Nutricional, MetodoPago, Venta, DetalleVenta
from django.contrib.auth.hashers import make_password
from decimal import Decimal

class Command(BaseCommand):
    help = 'Seed database with initial data'

    def handle(self, *args, **kwargs):
        # Roles
        admin_rol, _ = Rol.objects.get_or_create(nombre='Admin', descripcion='Administrador del sistema')
        cliente_rol, _ = Rol.objects.get_or_create(nombre='Cliente', descripcion='Cliente de la fornería')

        # Categorías
        panaderia, _ = Categoria.objects.get_or_create(nombre='Panadería', descripcion='Pan dulce y salado')
        pasteleria, _ = Categoria.objects.get_or_create(nombre='Pastelería', descripcion='Tortas y postres')
        bebidas, _ = Categoria.objects.get_or_create(nombre='Bebidas', descripcion='Bebidas calientes y frías')

        # Direcciones
        dir_admin, _ = Direccion.objects.get_or_create(
            calle='Av. Principal', 
            numero='123', 
            comuna='Santiago', 
            region='RM'
        )
        dir_cliente, _ = Direccion.objects.get_or_create(
            calle='Calle Secundaria', 
            numero='456', 
            comuna='Providencia', 
            region='RM'
        )

        # Información nutricional
        nutricional_pan, _ = Nutricional.objects.get_or_create(
            ingredientes='Harina, agua, sal, levadura',
            tiempo_preparacion=120,
            proteinas=8.5,
            azucar=2.0,
            gluten=True
        )

        nutricional_torta, _ = Nutricional.objects.get_or_create(
            ingredientes='Harina, huevos, azúcar, mantequilla',
            tiempo_preparacion=180,
            proteinas=6.2,
            azucar=25.0,
            gluten=True
        )

        # Métodos de pago
        efectivo, _ = MetodoPago.objects.get_or_create(nombre='Efectivo')
        tarjeta, _ = MetodoPago.objects.get_or_create(nombre='Tarjeta')
        transferencia, _ = MetodoPago.objects.get_or_create(nombre='Transferencia')

        # Productos
        pan_marraqueta, _ = Producto.objects.get_or_create(
            nombre='Marraqueta',
            marca='La Fornería',
            precio=Decimal('1200.00'),
            tipo='Propia',
            categoria=panaderia,
            stock_actual=50,
            nutricional=nutricional_pan
        )

        torta_chocolate, _ = Producto.objects.get_or_create(
            nombre='Torta de Chocolate',
            marca='La Fornería',
            precio=Decimal('8500.00'),
            tipo='Propia',
            categoria=pasteleria,
            stock_actual=5,
            nutricional=nutricional_torta
        )

        cafe_americano, _ = Producto.objects.get_or_create(
            nombre='Café Americano',
            marca='La Fornería',
            precio=Decimal('1800.00'),
            tipo='Propia',
            categoria=bebidas,
            stock_actual=100
        )

        # Usuarios
        admin_user, created = Usuario.objects.get_or_create(
            username='admin',
            email='admin@forneria.cl',
            defaults={
                'first_name': 'Admin',
                'paterno': 'Sistema',
                'run': '11111111-1',
                'is_staff': True,
                'is_superuser': True,
                'direccion': dir_admin,
                'rol': admin_rol
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()

        cliente_user, created = Usuario.objects.get_or_create(
            username='cliente',
            email='cliente@forneria.cl',
            defaults={
                'first_name': 'Juan',
                'paterno': 'Pérez',
                'run': '22222222-2',
                'is_staff': True,  # Para acceder al admin
                'is_superuser': False,
                'direccion': dir_cliente,
                'rol': cliente_rol
            }
        )
        if created:
            cliente_user.set_password('cliente123')
            cliente_user.save()

        # Ventas de ejemplo
        venta1, _ = Venta.objects.get_or_create(
            usuario=cliente_user,
            metodo_pago=tarjeta,
            monto_total=Decimal('1200.00'),
            estado='Pagado',
            canal_venta='Local'
        )

        venta2, _ = Venta.objects.get_or_create(
            usuario=cliente_user,
            metodo_pago=efectivo,
            monto_total=Decimal('8500.00'),
            estado='Pendiente',
            canal_venta='Instagram'
        )

        # Detalles de venta
        DetalleVenta.objects.get_or_create(
            venta=venta1,
            producto=pan_marraqueta,
            cantidad=1,
            precio_unitario=Decimal('1200.00')
        )

        DetalleVenta.objects.get_or_create(
            venta=venta2,
            producto=torta_chocolate,
            cantidad=1,
            precio_unitario=Decimal('8500.00')
        )

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
        self.stdout.write(self.style.SUCCESS('Users created:'))
        self.stdout.write(f'  - Admin: admin@forneria.cl / admin123')
        self.stdout.write(f'  - Cliente: cliente@forneria.cl / cliente123')
