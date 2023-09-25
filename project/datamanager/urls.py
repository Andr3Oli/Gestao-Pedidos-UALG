from django.urls import path

from datamanager.views import *

urlpatterns = [
    path('importDSD/', import_DSD, name='import_DSD'),
    path('importDOCENTE/', importdocentesxls, name='import_DOCENTE'),
    path('importRUC/', import_RUC, name='import_RUC'),
    path('importSalas', import_salas, name='import_salas'),
    path('export/', export_pedidos_xls, name='export_pedidos_xls'),
    path('sucesso/', sucesso_view, name='sucesso'),
]
