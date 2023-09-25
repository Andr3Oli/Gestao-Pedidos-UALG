from django.urls import path


from funcionariomanager.views import *

urlpatterns = [
    path('createAnoletivo/', create_anoletivo, name='create_anoletivo'),
    path('selectAnoLetivo/', selectanoletivo, name='select_ANOLETIVO'),
    path('sucesso/', sucesso_view, name='sucesso'),
    path('erro/', erro_view, name='erro'),
    path('delete_anoLetivo/<int:id>', delete_anoletivo, name="deleteAnoLetivo"),
    path('anoLetivo/', RenderAnoLetivo, name='list_anoletivo'),
    path('edit_anoLetivo/<int:id>', edit_anoletivo, name="editAnoLetivo"), 
    path('email_PCP/<int:ppd_ID>', emailPCP, name="emailPCP"),
    path('app/<int:user_id>', app_render.as_view(template_name="funcionariomanager/app.html"), name='app_render'),
    path('consult_pedidoSala/<int:pedidoID>', consult_pedidoSala, name='consult_pedidoSala'),
    path('consult_pedido/<int:pdd_id>', consult_pedido, name='consult_pedido'),
    path('consult_pedidoHorario/<int:pdd_id>', consult_pedidoHorario, name='consult_pedido'),
    path('consult_pedidoUnidadeCurricular/<int:id>', consult_unidadeCurricular, name='consult_pedidoUC'),
    path('confirmation/resolve/<int:pdd_id>', resolve_pedido, name='resolve_pedido'),    
    path('confirmation/link/<int:pdd_id>', link_pedido, name='link_pedido'),
    path('confirmation/cancel/<int:pdd_id>', cancela_pedido, name='cancela_pedido'),
    path('confirmation/desassocia/<int:pdd_id>', desassocia_pedido, name='desassocia_pedido'),
    path('rejection_message/', msg_motivo, name='rejection_message/')
]