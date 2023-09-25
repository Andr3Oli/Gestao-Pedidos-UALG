from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
from datetime import *
from datetime import date

from django_tables2 import *
from .tables import *

from django.contrib import messages
from django.core.mail import EmailMessage

from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from funcionariomanager.filters import *
from dateutil.relativedelta import relativedelta


#################################################
##### Ordem:                                #####
#####      -Envio de Informação para PCP    #####
#####      -Criar/ selecionar Ano Letivo    #####
#####      -Listar Ano Letivo               #####
#####      -Editar Ano Letivo               #####
#####      -Apagar Ano Letivo               #####
#####      -View Sucesso                    #####
#################################################

###################################################################################
######### Envio de Informação para PCP  ###########################################
######### Autor: André Oliveira         ###########################################
###################################################################################

def emailPCP(request, ppd_ID):
    if not request.user.is_authenticated:
        return redirect('/requestmanager/welcome/')

    pedido = Pedido.objects.get(id=ppd_ID)
    if request.method == 'POST':
        form = email_PCP(request.POST)
        if form.is_valid():
            assunto = request.POST.get('assunto')
            descricao = request.POST.get('descricao')
            link = ""
            if "Outros" in str(pedido.tipo):
                link = "link pedido: http://127.0.0.1:8000/funcionariomanager/consult_pedido/" + str(ppd_ID) + "\n"
            if "Salas" in str(pedido.tipo):
                link = "link pedido: http://127.0.0.1:8000/funcionariomanager/consult_pedidoSala/" + str(ppd_ID) + "\n"
            if "Unidades" in str(pedido.tipo):
                link = "link pedido: http://127.0.0.1:8000/funcionariomanager/consult_pedidoUnidadeCurricular/" + str(
                    ppd_ID) + "\n"
            if "Horários" in str(pedido.tipo):
                link = "link pedido: http://127.0.0.1:8000/funcionariomanager/consult_pedidoHorario/" + str(
                    ppd_ID) + "\n"
            nova_descricao = link + descricao
            email = EmailMessage(assunto, nova_descricao, 'a72707@ualg.pt', ['a72707@ualg.pt'])
            email.send()

            messages.info(request, 'Email enviado com sucesso')
            return redirect('/funcionariomanager/app/' + str(request.user.id))
    else:
        form = email_PCP()
    return render(request, 'funcionariomanager/email_PCP.html', {'form': form})


###################################################################################
######### Criar/ selecionar Ano letivo  ###########################################
######### Autor: António Madureira      ###########################################
###################################################################################

def create_anoletivo(request):
    if not request.user.is_authenticated:
        return redirect('/requestmanager/welcome/')

    if request.method == 'POST':
        form = create_AnoLetivo(request.POST)
        if form.is_valid():
            datainicio = form.cleaned_data['datainicio']
            datafim = form.cleaned_data['datafim']

            anoinicio = str(datainicio.year)
            anofim = str(datafim.year)

            minimo = str(datainicio + relativedelta(months=+8))
            maximo = str(datainicio + relativedelta(months=+12))

            if (datainicio >= datafim):
                messages.info(request, 'A data de inicio deve ser antes da data final!')
                return HttpResponseRedirect('/funcionariomanager/createAnoletivo')

            if not ((minimo <= str(datafim)) and (str(datafim) <= maximo)):
                messages.info(request, 'Os anos letivos devem ter um minimo de 8 meses e um maximo de um ano!')
                return HttpResponseRedirect('/funcionariomanager/createAnoletivo')

            name = str(anoinicio) + "-" + (str(anofim))[2:4]
            if AnoLetivo.objects.filter(nome=name).count():
                print("Erro Dup")
                messages.info(request, 'O ano letivo já existe!')
                return HttpResponseRedirect('/funcionariomanager/createAnoletivo')

            # Objeto AnoLetivo
            anoletivo = AnoLetivo()
            anoletivo.nome = name
            anoletivo.datainicio = datainicio
            anoletivo.datafim = datafim
            anoletivo.save()
            messages.info(request, 'O ano letivo foi criado com sucesso.')
            return redirect('/funcionariomanager/anoLetivo/')
    else:
        form = edit_AnoLetivo()
    return render(request, 'funcionariomanager/create_anoletivo.html', {'form': form})


def selectanoletivo():
    today = date.today()
    print(today)
    anoletivo = AnoLetivo.objects.filter(datainicio__lt=today, datafim__gt=today)
    return anoletivo[0]

###################################################################################
######### Listar Ano letivo      ##################################################
######### Autor: Gonçalo Almeida ##################################################
###################################################################################

def RenderAnoLetivo(request):
    if not request.user.is_authenticated or not request.user.groups.filter(name="Funcionario").exists():
        return redirect('/requestmanager/welcome/')

    tables = AnoLetivoTable(AnoLetivo.objects.all())
    return render(request, 'funcionariomanager/list_anoletivo.html', {"table": tables})


###############################################################################
######### Edit Ano letivo   ###################################################
######### Autor: Tomás Roma ###################################################
###############################################################################

def edit_anoletivo(request, id):
    if not request.user.is_authenticated or not request.user.groups.filter(name="Funcionario"):
        return redirect('/requestmanager/welcome/')

    anoletivo = AnoLetivo.objects.get(id=id)
    if request.method == 'POST':
        form = edit_AnoLetivo(request.POST)
        if form.is_valid():
            datainicio = form.cleaned_data['datainicio']
            datafim = form.cleaned_data['datafim']

            anoi = datainicio.year
            anof = datafim.year

            if (anoi + 1 != anof):
                print("Erro Ano")
                messages.error(request, 'Os anos letivos devem ter um maximo de um ano!')
                return HttpResponseRedirect('/funcionariomanager/edit_anoLetivo/' + str(id))
            name = str(anoi) + "-" + (str(anof))[2:4]
            if AnoLetivo.objects.filter(nome=name, datainicio=datainicio, datafim=datafim).count() != 0:
                print("Erro Dup")
                messages.error(request, 'O ano letivo já existe!')
                return HttpResponseRedirect('/funcionariomanager/edit_anoLetivo/' + str(id))

            pedidosAno = Pedido.objects.filter(anoletivo=id)
            if pedidosAno.count():
                print("Erro pedido")
                messages.error(request, 'Ja exitem pedidos associados ao ano letivo.')
                return HttpResponseRedirect('/funcionariomanager/edit_anoLetivo/' + str(id))

            anoletivo.nome = name
            anoletivo.datainicio = datainicio
            anoletivo.datafim = datafim
            anoletivo.save()
            messages.info(request, 'O ano letivo foi editado com sucesso.')
            return HttpResponseRedirect('/funcionariomanager/anoLetivo/')

    form = edit_AnoLetivo(initial={
        'datainicio': anoletivo.datainicio,
        'datafim': anoletivo.datafim
    })
    context = {
        "form": form,
        "name": anoletivo.nome,
    }
    return render(request, 'funcionariomanager/edit_anoletivo.html', context)


###################################################################################
######### Delete Ano letivo     ###################################################
######### Autor: André Oliveira ###################################################
###################################################################################

def delete_anoletivo(request, id):
    if not request.user.is_authenticated:
        return redirect('/requestmanager/welcome/')

    anoletivo = AnoLetivo.objects.get(id=id)
    pedidosAno = Pedido.objects.filter(anoletivo=id)
    if pedidosAno.count():
        messages.error(request, 'Não foi possível eliminar o ano letivo. Já tem pedidos associados.')
        return HttpResponseRedirect('/funcionariomanager/anoLetivo/')
    if request.method == 'POST':
        anoletivo.delete()
        messages.info(request, 'O ano letivo foi eliminado com sucesso.')
        return HttpResponseRedirect('/funcionariomanager/anoLetivo/')
    return render(request, 'funcionariomanager/delete_anoletivo.html')


# Mensagem de sucesso

def sucesso_view(request, mensagem):
    if not request.user.is_authenticated:
        return redirect('/requestmanager/welcome/')

    return render(request, 'funcionariomanager/sucesso.html', {'message': mensagem})


def erro_view(request, mensagem):
    if not request.user.is_authenticated:
        return redirect('/requestmanager/welcome/')

    return render(request, 'funcionariomanager/erro.html', {'message': mensagem})


class app_render(SingleTableMixin, django_filters.views.FilterView):
    model = Pedido
    table_class = PedidoTable
    filterset_class = PedidoFilter
    template_name = 'funcionariomanager/app.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/requestmanager/welcome/')
        elif request.user.groups.filter(name='ProfessorUniversitario').exists():
            return redirect('/requestmanager/app/' + str(request.user.id))

        return super().dispatch(request, *args, **kwargs)

    # def get_queryset(self):
    #     return Pedido.objects.all().filter(responsavel__pedido__id=self.kwargs['user_id'])


def consult_pedido(request, pdd_id):
    if not request.user.is_authenticated:
        return redirect('/requestmanager/welcome/')

    pedido = Pedido.objects.get(pk=pdd_id)
    all_pedidos = Pedidooutros.objects.filter(pedido_ptr_id=pedido)

    context = {
        "id": pdd_id,
        "Assunto": pedido.assunto,
        "Descrição": pedido.descricao,
        "Data_alvo": pedido.dataalvo,
        'all_pedidos': all_pedidos,
        'isStateChangeable': pedido.anoletivo == selectanoletivo() and pedido.estado_id != 3,
        'pendente': pedido.anoletivo == selectanoletivo() and pedido.estado_id == 1,
        'resolvido': pedido.anoletivo == selectanoletivo() and pedido.estado_id != 3 and pedido.estado_id == 2,
        'check': pedido.responsavel.id == request.user.id
    }
    return render(request, 'funcionariomanager/consult_pedido.html', context)


def consult_pedidoSala(request, pedidoID):
    if not request.user.is_authenticated:
        return redirect('/requestmanager/welcome/')

    pedido = Pedido.objects.get(pk=pedidoID)
    context = {
        "id": pedidoID,
        'pendente': pedido.anoletivo == selectanoletivo() and pedido.estado_id == 1,
        'resolvido': pedido.anoletivo == selectanoletivo() and pedido.estado_id != 3 and pedido.estado_id == 2,
        'check': pedido.responsavel.id == request.user.id
    }
    return render(request, 'funcionariomanager/consult_pedidosala.html', context)


def consult_unidadeCurricular(request, id):
    if not request.user.is_authenticated:
        return redirect('/requestmanager/welcome/')

    pedido = Pedido.objects.get(id=id)
    form = PedidoForm(initial={'assunto': pedido.assunto, 'descricao': pedido.descricao, 'data': pedido.dataalvo})
    context = {
        'id': id,
        'form': form,
        'pendente': pedido.anoletivo == selectanoletivo() and pedido.estado_id == 1,
        'resolvido': pedido.anoletivo == selectanoletivo() and pedido.estado_id != 3 and pedido.estado_id == 2,
        'check': pedido.responsavel.id == request.user.id
    }
    return render(request, 'funcionariomanager/consult_unidadecurricular.html', context)


def consult_pedidoHorario(request, pdd_id):
    if not request.user.is_authenticated:
        return redirect('/requestmanager/welcome/')

    pedido = Pedido.objects.get(pk=pdd_id)
    context = {
        "id": pdd_id,
        'pendente': pedido.anoletivo == selectanoletivo() and pedido.estado_id == 1,
        'resolvido': pedido.anoletivo == selectanoletivo() and pedido.estado_id != 3 and pedido.estado_id == 2,
        'check': pedido.responsavel.id == request.user.id
    }
    return render(request, 'funcionariomanager/consult_pedidoHorario.html', context)


def cancela_pedido(request, pdd_id):
    if not request.user.is_authenticated or not request.user.groups.filter(name="Funcionario"):
        return redirect('/requestmanager/welcome/')
    return msg_motivo(request, pdd_id)


def desassocia_pedido(request, pdd_id):
    if not request.user.is_authenticated or not request.user.groups.filter(name="Funcionario"):
        return redirect('/requestmanager/welcome/')

    if request.method == 'POST':
        pedido = Pedido.objects.get(pk=pdd_id)
        pedido.estado = EstadoPedido.objects.get(pk=1)
        pedido.dataatribuicao = None
        pedido.responsavel = None
        pedido.save()
        messages.info(request, 'O pedido foi desassociado com sucesso.')
        return redirect('/funcionariomanager/app/' + str(request.user.id))
    context = {
        "id": pdd_id,
        'confirm_question': "Tem a certeza que quer desassociar-se do pedido?"
    }
    return render(request, 'funcionariomanager/confirmation-page.html', context)


def resolve_pedido(request, pdd_id):
    if not request.user.is_authenticated:
        return redirect('/requestmanager/welcome/')

    if request.method == 'POST':
        pedido = Pedido.objects.get(pk=pdd_id)
        pedido.estado_id = 3
        da = datetime.now(timezone.utc) + relativedelta(hours=+1)
        print(da)
        pedido.dataresolvido = da
        pedido.tempoespera = da - pedido.datacriacao
        print(da - pedido.datacriacao)
        pedido.tempoprocesso = da - pedido.dataatribuicao
        print(da - pedido.dataatribuicao)
        pedido.save()
        messages.info(request, 'O pedido foi aceite com sucesso.')
        return redirect('/funcionariomanager/app/' + str(request.user.id))
    context = {
        "id": pdd_id,
        'confirm_question': "Tem a certeza que quer aceitar o pedido?"
    }
    return render(request, 'funcionariomanager/confirmation-page.html', context)


def link_pedido(request, pdd_id):
    if not request.user.is_authenticated:
        return redirect('/requestmanager/welcome/')

    if request.method == 'POST':
        pedido = Pedido.objects.get(pk=pdd_id)
        res = Funcionario.objects.get(pk=request.user.id)
        pedido.responsavel = res
        pedido.dataatribuicao = datetime.now()
        pedido.estado = EstadoPedido.objects.get(pk=2)
        pedido.save()
        messages.info(request, 'O pedido foi associado com sucesso.')
        return redirect('/funcionariomanager/app/' + str(request.user.id))

    context = {
        "id": pdd_id,
        'confirm_question': "Tem a certeza que quer associar-se ao pedido?"
    }
    return render(request, 'funcionariomanager/confirmation-page.html', context)

def msg_motivo(request, pdd_id):
    if request.method == 'POST':
        form = messageForm(request.POST)
        if form.is_valid():
            messagem = form.cleaned_data['messagem']
            pedido = Pedido.objects.get(pk=pdd_id)
            pedido.estado_id = 4
            da = datetime.now(timezone.utc) + relativedelta(hours=+1)
            pedido.dataresolvido = da
            pedido.tempoespera = da - pedido.datacriacao
            pedido.tempoprocesso = da - pedido.dataatribuicao
            pedido.motivocancelmento = messagem
            pedido.save()
            messages.info(request, 'O pedido foi rejeitado com sucesso.')
            return redirect('/funcionariomanager/app/' + str(request.user.id))


    form = messageForm()
    return render(request, 'funcionariomanager/messagem_cancel.html', {'form':form})
