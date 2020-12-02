from django.contrib import admin

# Register your models here.
from .models import User, Paciente, Turno, Producto, Categoria, Pedido, DetallePedido

admin.site.register(User)
admin.site.register(Paciente)
admin.site.register(Turno)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Pedido)
admin.site.register(DetallePedido)