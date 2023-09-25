from django.urls import path

from requestmanager.views import *

urlpatterns = [
    path('pedidoHorario/', create_pedidoHorario, name='create_pedidoHorario'),
    path('editarPedidoHorario/<int:pdd_id>', edit_pedidoHorario, name='edit_pedidoHorario'),
    # path('apagarPedidoHorario/<int:pdd_id>', delete_pedidoHorario, name='delete_pedidoHorario'),
    path('createpedidooutro/', create_pedidooutro, name='create_pedidooutro'),
    # path('deletepedidooutro/', delete_pedidooutro, name='delete_pedidooutro'),
    path('editpedidooutro/<int:pdd_id>', edit_pedidooutro, name='edit_pedidooutro'),
    path('create_pedidoUnidadeCurricular/', create_unidadeCurricular, name='create_unidadeCurricular'),
    # path('delete_pedidoUnidadeCurricular/<int:pedidoID>', delete_unidadeCurricular, name='delete_unidadeCurricular'),
    path('edit_pedidoUnidadeCurricular/<int:pedidoID>', edit_unidadeCurricular, name='edit_unidadeCurricular'),
    path('list_pedidoUnidadeCurricular/<int:user_id>', app_renderUC.as_view(template_name="requestmanager/list_unidadecurricular.html"), name='list_unidadeCurricular'),
    path('list_salas/<int:user_id>', app_renderSalas.as_view(template_name="requestmanager/list_salas.html"), name='list_salas'),
    path('list_horario/<int:user_id>', app_renderHorario.as_view(template_name="requestmanager/list_horario.html"), name='list_horario'),
    path('list_outros/<int:user_id>', app_renderOutros.as_view(template_name="requestmanager/list_outros.html"), name='list_outros'),
    # path('delete_pedidoSala/', delete_pedidoSala, name='delete_pedidoSala'),
    path('create_pedidoSala/', create_pedidoSala, name='create_pedidoSala'),
    path('edit_pedidoSala/<int:pedidoID>', edit_pedidoSala, name='edit_pedidoSala'),
    path('consult_pedido/<int:pdd_id>', consult_pedido, name='consult_pedido'),
    path('delete_pedido/<int:pdd_id>', delete_pedido, name='delete_pedido'),
    path('app/<int:user_id>', app_render.as_view(template_name="requestmanager/app.html"), name='app_render'),
    path('consult_pedidoSala/<int:pedidoID>', consult_pedidoSala, name='consult_pedidoSala'),
    path('consult_pedido/<int:pdd_id>', consult_pedido, name='consult_pedido'),
    path('consult_pedidoHorario/<int:pdd_id>', consult_pedidoHorario, name='consult_pedido'),
    path('consult_pedidoUnidadeCurricular/<int:id>', consult_unidadeCurricular, name='consult_pedidoUC'),
    path('delete_pedido/<int:id>', delete_pedido, name='delete_pedido'),
    path('sucesso/', sucesso_view, name='sucesso'),
    path('welcome/', welcome_page_view, name='welcome_page')
]
