from django.urls import path

from .views import *

urlpatterns = [
    path('funcionarios_stats/', funcionarios_stats, name='funcionarios_stats'),
    path('chart_pedidos/', chart.as_view(), name='chart_pedidos'),
    path('chart_data/', chartPedidos.as_view(), name='chart_data'),
    
    path('funcionarios_data/', average_pedidos_timerange, name='fixe'),
    path('pedidos_media/', pedidos_media, name='pedidos_media'),
    path('lchartdata/', getLineChartData, name ='lchartdata'),
    path('lchartdata2/', getLineChartAfterCheck, name='lchartdata2')
]
