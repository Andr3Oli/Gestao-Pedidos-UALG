from django.contrib import admin
from django.urls import include, path
from .views import *

urlpatterns = [
    path('pedido/<int:id>', PedidoDetailAPIView.as_view()),
    path('pedido/', PedidoAPIView.as_view()),
    path('pedido_outro/<int:id>', PedidoOutrosDetailAPIView.as_view()),
    path('pedido_outro/', PedidoOutroAPIView.as_view()),
    path('uc_unidadecurricular/<int:id>', UnidadeCurricularAPIView.as_view()),
    path('pedido_uc/<int:id>', PedidoUCDetailAPIView.as_view()),
    path('acao/', AcaoAPIView.as_view()),
    path('categoriaSala/', CategoriaSalaAPIView.as_view()),
    path('pedido_sala/<int:id>', PedidoSalaDetailAPIView.as_view()),
    path('pedido_horario/<int:id>', PedidoHorarioDetailAPIView.as_view()),
    path('funcionarios/', FuncionarioAPIView.as_view()),
    path('tipopedidosala/', TipoPedidoSalaAPIView.as_view()),
    path('tipoturma/', TipoTurmaAPIView.as_view())
]