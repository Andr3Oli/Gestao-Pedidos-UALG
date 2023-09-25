import django_tables2 as tables
from .models import *
from django.utils.html import format_html
from django_filters import *
from dateutil.relativedelta import relativedelta


#################################################
##### Ordem:                                #####
#####      -Listar Pedidos Geral            #####
#####      -Listar Pedidos UC               #####
#####      -Listar Pedidos Outros           #####
#####      -Listar Pedidos Sala             #####
#####      -Listar Pedidos Horario          #####
#################################################

###################################################################################
######### Listar Pedidos Geral         ###########################################
###################################################################################

class PedidoTable(tables.Table):
    class Meta:
        model = Pedido
        template_name = "django_tables2/bootstrap.html"
        fields = ("assunto", "dataalvo", "tipo", "estado", "anoletivo","responsavel")
        
    tempo_espera = tables.TemplateColumn(template_name='templates/requestmanager/app.html', orderable=False)

    column = tables.TemplateColumn(verbose_name=(''),
                                   template_name='templates/requestmanager/app.html',
                                   orderable=False,
                                   )
    # PCP = tables.TemplateColumn(verbose_name=(''),
    #                                template_name='templates/requestmanager/app.html',
    #                                orderable=False,
    #                                )
    
    def render_tempo_espera(self, record):
        if(record.estado_id != 3 and record.estado_id != 4):
            value = str((datetime.now(timezone.utc) + relativedelta(hours=+1)) - record.datacriacao)
            lenght = len(value)
            value = value[:lenght - 6]
            value = value.replace(':', 'h', 1)
            value = value.replace(':', 'm', 1)
            value = value.replace('.', 's', 1)
            value = value.replace('days', 'dias', 1)
            value = value.replace('day', 'dia', 1)
        else:
            value = str(record.tempoespera)
            lenght = len(value)
            value = value[:lenght - 6]
            value = value.replace(':', 'h', 1)
            value = value.replace(':', 'm', 1)
            value = value.replace('.', 's', 1)
            value = value.replace('days', 'dias', 1)
            value = value.replace('day', 'dia', 1)
        return format_html("<b>{}</b>", value) 

    def render_column(self, record):
        if (str(record.tipo) == "Horários"):
            return format_html(
                ''' <a href="/requestmanager/consult_pedidoHorario/%s  "  class="btn btn-success"><div class="icon-text">
                    <span><strong>Consultar</strong></span>
                    <span class="icon">
                        <i class="fas fa-info-circle"></i>
                    </span>
                    </div> </a>''' % (
                    record.pk))
        elif (str(record.tipo) == "Outros"):
            return format_html(
                ''' <a href="/requestmanager/consult_pedido/%s  "  class="btn btn-success"><div class="icon-text">
                    <span><strong>Consultar</strong></span>
                    <span class="icon">
                        <i class="fas fa-info-circle"></i>
                    </span>
                    </div></a>''' % (
                    record.pk))
        elif (str(record.tipo) == "Salas"):
            return format_html(
                ''' <a href="/requestmanager/consult_pedidoSala/%s  "  class="btn btn-success"><div class="icon-text">
                    <span><strong>Consultar</strong></span>
                    <span class="icon">
                        <i class="fas fa-info-circle"></i>
                    </span>
                    </div></a>''' % (
                    record.pk))
        elif (str(record.tipo) == "Unidades Curriculares"):
            return format_html(
                ''' <a href="/requestmanager/consult_pedidoUnidadeCurricular/%s  "  class="btn btn-success"><div class="icon-text">
                    <span><strong>Consultar</strong></span>
                    <span class="icon">
                        <i class="fas fa-info-circle"></i>
                    </span>
                    </div></a>''' % (
                    record.pk))
            
    # def render_PCP(self, record):
    #     return format_html(
    #             ''' <a href="/funcionariomanager/email_PCP/%s" class="btn btn-success"> | PCP </a>''' % (
    #                 record.pk))
    

###################################################################################
######### Listar Pedidos UC             ###########################################
######### Autor: André Oliveira         ###########################################
###################################################################################

class PedidoTableUC(tables.Table):
    class Meta:
        model = Pedido
        template_name = "django_tables2/bootstrap.html"
        fields = ("assunto", "dataalvo", "estado", "responsavel")

    tempo_espera = tables.TemplateColumn(template_name='templates/requestmanager/app.html')

    column = tables.TemplateColumn(verbose_name=(''),
                                   template_name='templates/requestmanager/app.html',
                                   orderable=False,
                                   )
    # PCP = tables.TemplateColumn(verbose_name=(''),
    #                                template_name='templates/requestmanager/app.html',
    #                                orderable=False,
    #                                )
    
    def render_tempo_espera(self, record):
        if(record.estado_id != 3 and record.estado_id != 4):
            value = str((datetime.now(timezone.utc) + relativedelta(hours=+1)) - record.datacriacao)
            lenght = len(value)
            value = value[:lenght - 6]
            value = value.replace(':', 'h', 1)
            value = value.replace(':', 'm', 1)
            value = value.replace('.', 's', 1)
            value = value.replace('days', 'dias', 1)
            value = value.replace('day', 'dia', 1)
        else:
            value = str(record.tempoespera)
            lenght = len(value)
            value = value[:lenght - 6]
            value = value.replace(':', 'h', 1)
            value = value.replace(':', 'm', 1)
            value = value.replace('.', 's', 1)
            value = value.replace('days', 'dias', 1)
            value = value.replace('day', 'dia', 1)
        return format_html("<b>{}</b>", value) 

    def render_column(self, record):
        return format_html(
            ''' <a href="/requestmanager/consult_pedidoUnidadeCurricular/%s  "  class="btn btn-success"><div class="icon-text">
                    <span><strong>Consultar</strong></span>
                    <span class="icon">
                        <i class="fas fa-info-circle"></i>
                    </span>
                    </div></a>''' % (
                record.pk))
    # def render_PCP(self, record):
    #     return format_html(
    #             ''' <a href="/funcionariomanager/email_PCP/%s" class="btn btn-success"> | PCP </a>''' % (
    #                 record.pk))


###################################################################################
######### Listar Pedidos Outros         ###########################################
######### Autor: Gonçalo Almeida        ###########################################
###################################################################################

class PedidoTableOutros(tables.Table):
    class Meta:
        model = Pedidooutros
        template_name = "django_tables2/bootstrap.html"
        fields = ("assunto", "dataalvo", "estado", "responsavel")

    tempo_espera = tables.TemplateColumn(template_name='templates/requestmanager/app.html')

    column = tables.TemplateColumn(verbose_name=(''),
                                   template_name='templates/requestmanager/app.html',
                                   orderable=False,
                                   )
    # PCP = tables.TemplateColumn(verbose_name=(''),
    #                                template_name='templates/requestmanager/app.html',
    #                                orderable=False,
    #                                )
                                   
    def render_tempo_espera(self, record):
        if(record.estado_id != 3 and record.estado_id != 4):
            value = str((datetime.now(timezone.utc) + relativedelta(hours=+1)) - record.datacriacao)
            lenght = len(value)
            value = value[:lenght - 6]
            value = value.replace(':', 'h', 1)
            value = value.replace(':', 'm', 1)
            value = value.replace('.', 's', 1)
            value = value.replace('days', 'dias', 1)
            value = value.replace('day', 'dia', 1)
        else:
            value = str(record.tempoespera)
            lenght = len(value)
            value = value[:lenght - 6]
            value = value.replace(':', 'h', 1)
            value = value.replace(':', 'm', 1)
            value = value.replace('.', 's', 1)
            value = value.replace('days', 'dias', 1)
            value = value.replace('day', 'dia', 1)
        return format_html("<b>{}</b>", value) 

    def render_column(self, record):
        return format_html(
            ''' <a href="/requestmanager/consult_pedido/%s  "  class="btn btn-success"><div class="icon-text">
                    <span><strong>Consultar</strong></span>
                    <span class="icon">
                        <i class="fas fa-info-circle"></i>
                    </span>
                    </div></a>''' % (
                record.pk))
        
    # def render_PCP(self, record):
    #     return format_html(
    #             ''' <a href="/funcionariomanager/email_PCP/%s" class="btn btn-success"> | PCP </a>''' % (
    #                 record.pk))


###################################################################################
######### Listar Pedidos de Sala        ###########################################
######### Autor: António Madureira      ###########################################
###################################################################################

class PedidoTableSalas(tables.Table):
    class Meta:
        model = Pedido
        template_name = "django_tables2/bootstrap.html"
        fields = ("assunto", "dataalvo", "estado", "responsavel")
    
    tempo_espera = tables.TemplateColumn(template_name='templates/requestmanager/app.html')

    column = tables.TemplateColumn(verbose_name=(''),
                                   template_name='templates/requestmanager/app.html',
                                   orderable=False,
                                   )
    # PCP = tables.TemplateColumn(verbose_name=(''),
    #                                template_name='templates/requestmanager/app.html',
    #                                orderable=False,
    #                                )

    def render_tempo_espera(self, record):
        if(record.estado_id != 3 and record.estado_id != 4):
            value = str((datetime.now(timezone.utc) + relativedelta(hours=+1)) - record.datacriacao)
            lenght = len(value)
            value = value[:lenght - 6]
            value = value.replace(':', 'h', 1)
            value = value.replace(':', 'm', 1)
            value = value.replace('.', 's', 1)
            value = value.replace('days', 'dias', 1)
            value = value.replace('day', 'dia', 1)
        else:
            value = str(record.tempoespera)
            lenght = len(value)
            value = value[:lenght - 6]
            value = value.replace(':', 'h', 1)
            value = value.replace(':', 'm', 1)
            value = value.replace('.', 's', 1)
            value = value.replace('days', 'dias', 1)
            value = value.replace('day', 'dia', 1)
        return format_html("<b>{}</b>", value) 

    def render_column(self, record):
        return format_html(
            ''' <a href="/requestmanager/consult_pedidoSala/%s  "  class="btn btn-success"><div class="icon-text">
                    <span><strong>Consultar</strong></span>
                    <span class="icon">
                        <i class="fas fa-info-circle"></i>
                    </span>
                    </div></a>''' % (
                record.pk))
    
    # def render_PCP(self, record):
    #     return format_html(
    #             ''' <a href="/funcionariomanager/email_PCP/%s" class="btn btn-success"> | PCP </a>''' % (
    #                 record.pk))


###################################################################################
######### Pedidos Horario               ###########################################
######### Autor: Tomás Roma             ###########################################
###################################################################################

class PedidoTableHorario(tables.Table):
    class Meta:
        model = Pedido
        template_name = "django_tables2/bootstrap.html"
        fields = ("assunto", "dataalvo", "estado", "responsavel")

    tempo_espera = tables.TemplateColumn(template_name='templates/requestmanager/app.html')

    column = tables.TemplateColumn(verbose_name=(''),
                                   template_name='templates/requestmanager/app.html',
                                   orderable=False,
                                   )
    # PCP = tables.TemplateColumn(verbose_name=(''),
    #                                template_name='templates/requestmanager/app.html',
    #                                orderable=False,
    #                                )
    
    def render_tempo_espera(self, record):
        if(record.estado_id != 3 and record.estado_id != 4):
            value = str((datetime.now(timezone.utc) + relativedelta(hours=+1)) - record.datacriacao)
            lenght = len(value)
            value = value[:lenght - 6]
            value = value.replace(':', 'h', 1)
            value = value.replace(':', 'm', 1)
            value = value.replace('.', 's', 1)
            value = value.replace('days', 'dias', 1)
            value = value.replace('day', 'dia', 1)
        else:
            value = str(record.tempoespera)
            lenght = len(value)
            value = value[:lenght - 6]
            value = value.replace(':', 'h', 1)
            value = value.replace(':', 'm', 1)
            value = value.replace('.', 's', 1)
            value = value.replace('days', 'dias', 1)
            value = value.replace('day', 'dia', 1)
        return format_html("<b>{}</b>", value) 

    def render_column(self, record):
        return format_html(
            ''' <a href="/requestmanager/consult_pedidoHorario/%s  "  class="btn btn-success"><div class="icon-text">
                    <span><strong>Consultar</strong></span>
                    <span class="icon">
                        <i class="fas fa-info-circle"></i>
                    </span>
                    </div></a>''' % (
                record.pk))
    
    # def render_PCP(self, record):
    #     return format_html(
    #             ''' <a href="/funcionariomanager/email_PCP/%s" class="btn btn-success"> | PCP </a>''' % (
    #                 record.pk))
