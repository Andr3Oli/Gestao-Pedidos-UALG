import django_tables2 as tables
from requestmanager.views import *
from django.utils.html import format_html
from django_filters import *

class PedidoTable(tables.Table):
    amend = tables.TemplateColumn('<input type="checkbox" name="id" value="{{ record.pk }}" />', verbose_name="Select")
    class Meta:
        model = Pedido
        template_name = "django_tables2/bootstrap.html"
        fields = ("assunto", "dataalvo", "tipo", "estado", "anoletivo", "docente", "responsavel")
        
    def render_amend (self, record):
        return format_html(
            '<input name="id" type="checkbox" value="{}" />',
            record.pk)