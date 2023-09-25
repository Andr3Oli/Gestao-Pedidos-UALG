from django.contrib import admin

# Register your models here.
from .models import *

# admin.site.register(Funcionario)
admin.site.register(Sala)
admin.site.register(Categoriasala)
admin.site.register(Dsd)
admin.site.register(Pedido)
admin.site.register(Pedidohorario)
admin.site.register(Pedidooutros)
admin.site.register(Pedidosala)
admin.site.register(Pedidouc)
admin.site.register(Tipoalteracaohorario)
admin.site.register(Tipoconta)
admin.site.register(Tipopedidohorario)
admin.site.register(Unidadecurricular)
admin.site.register(EstadoPedido)
admin.site.register(TipoTurma)
admin.site.register(Tipopedidosala)