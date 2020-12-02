from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

ROLES = (
    ('M', 'Medico'),  
    ('S', 'Secretaria'),  
    ('G', 'Gerencia'), 
    ('V', 'Venta'),
    ('T', 'Taller') 
)

# Create your models here.
class User(AbstractUser):
    rol = models.CharField(max_length=1, default='S', choices=ROLES, verbose_name="Rol")
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Paciente(models.Model):
    apellido = models.CharField(max_length=25)
    nombre = models.CharField(max_length=25)
    documento = models.CharField(max_length=8)
    obra_social = models.CharField(max_length=30)
    medico = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        verbose_name="Médico", 
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"


class Turno(models.Model):

    HORARIOS = (
    ('1000', '10:00 hs'),  
    ('1030', '10:30 hs'),  
    ('1100', '11:00 hs'), 
    ('1130', '11:30 hs'),
    ('1200', '12:00 hs'),
    ('1230', '12:30 hs'),
    ('1300', '13:00 hs'),
    ('1330', '13:30 hs'),
    ('1400', '14:00 hs'),
    ('1430', '14:30 hs'),
    ('1500', '15:00 hs')
)
    
    paciente = models.ForeignKey(
        Paciente, 
        on_delete=models.CASCADE, 
        verbose_name="Paciente",
        related_name="turnos"
    )
    medico = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name="Médico",
        null=True
    )
    fecha = models.DateField(verbose_name="Fecha", default=timezone.now)
    horario = models.CharField(max_length=4, default='', choices=HORARIOS, verbose_name="Horario de Turno")
    #hora = models.TimeField()

    def __str__(self):
        return f"{self.paciente} {self.fecha} {self.horario}"


class Categoria(models.Model):
    nombre = models.CharField(max_length=250, verbose_name="Nombre de la categoria")

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.nombre


class Producto(models.Model):

    nombre = models.CharField(max_length=100, verbose_name="Nombre", unique=True)
    marca = models.CharField(max_length=50, verbose_name="Marca", blank=True, null=True)
    color = models.CharField(max_length=15, verbose_name="Color", blank=True, null=True)
    precio = models.DecimalField(max_digits=11, decimal_places=2, verbose_name="Precio")
    imagen = models.ImageField(upload_to='productos/%Y/%m/%d', blank=True, null=True, verbose_name="Imagen")
    stock = models.IntegerField(blank=True, null=True, verbose_name="Cantidad en Stock", default=1)
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.CASCADE, 
        blank=True,
        null=True,
        verbose_name="Categoria",
        )
    lado_izquierdo = models.BooleanField(default=False, verbose_name="Lente Lado Izquierdo")
    lado_derecho = models.BooleanField(default=False, verbose_name="Lente Lado Derecho")
    distancia_cerca = models.BooleanField(default=False, verbose_name="Lente de Cerca")
    distancia_lejos = models.BooleanField(default=False, verbose_name="Lente de Lejos")
    armazon = models.BooleanField(default=False, verbose_name="Con Armazón")
    
     
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return f"{self.nombre} | stock: {self.stock} | $ {self.precio} "



class Pedido(models.Model):

    ESTADOS_PEDIDOS = (
    ('P', 'Pendiente'),
    ('T', 'Taller'),
    ('F', 'Finalizado'),
    )

    OPCIONES_DE_PAGO = (
        ('TC', 'Tarjeta de credito'),
        ('BV', 'Billetera virtual'),
        ('EF', 'Efectivo'),
        ('DE', 'Debito'),
    )

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, verbose_name="Paciente")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    #producto = models.ManyToManyField(Producto, on_delete=models.CASCADE)
    preciototal = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0.0,
        verbose_name="Precio Total",
        blank=True,
        null=True
    )
    tipo_pago = models.CharField(max_length=20)
    estado = models.CharField(
        max_length=1,
        default='P',
        choices=ESTADOS_PEDIDOS,
        verbose_name="Estado actual del pedido"
    )
    tipo_de_pago = models.CharField(
        max_length=2,
        default='TC',
        choices=OPCIONES_DE_PAGO,
        verbose_name='Tipo de pago'
    )
    
    vendedor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name='Vendedor',
        related_name="ventas",
        blank=True,
        null=True
    )

    fecha = models.DateField(verbose_name="Fecha", blank=True, null=True)

    def __str__(self):
        return f"{self.paciente}"


class DetallePedido(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, blank=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, blank=True, null=True)
    cantidad = models.IntegerField(verbose_name="Cantidad", default=1)
    subtotal = models.DecimalField(max_digits=11,
                                decimal_places=2,
                                default=0.0,
                                blank=True,
                                verbose_name="Subtotal"
                                )

