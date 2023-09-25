import math
import time
import json
from django.views import View

import pytz
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from requestmanager.models import *
from .forms import *
from rest_framework.views import APIView
from rest_framework.response import Response
from requestmanager.views import selectanoletivo

def funcionarios_stats(request):
    if not request.user.is_authenticated or not request.user.groups.filter(name="Funcionario").exists():
        return redirect('/requestmanager/welcome/')
    return render(request, 'statmanager/average_pedido_form.html', {'error': ''})


def average_pedidos_timerange(request):
    if request.method == 'POST':
        print(request.body.decode("utf-8"))
        t = json.loads(request.body.decode("utf-8"))
        print(t)
        data_resolvidos = []
        data_aceites = []
        data_pendentes = []
        data_cancelados = []
        labels = []

        pendente = EstadoPedido.objects.get(pk=1)
        aceite = EstadoPedido.objects.get(pk=2)
        resolvido = EstadoPedido.objects.get(pk=3)
        cancelado = EstadoPedido.objects.get(pk=4)

        data_inicio = datetime.strptime(t['data_inicio'], '%Y-%m-%d').date().isoformat()
        data_fim = datetime.strptime(t['data_fim'], '%Y-%m-%d').date().isoformat()

        print(t['f'])
        lista = json.loads(t['f'])
        for obj in lista:
            print(obj)
            id_F = obj['id']
            funcionario = Funcionario.objects.get(pk=id_F)
            labels.append(funcionario.username)

            p2 = len(Pedido.objects.filter(responsavel=funcionario, estado=aceite, dataatribuicao__gte=data_inicio,
                                           dataatribuicao__lte=data_fim))
            p3 = len(Pedido.objects.filter(responsavel=funcionario, estado=resolvido, dataresolvido__gte=data_inicio,
                                           dataresolvido__lte=data_fim))
            p4 = len(Pedido.objects.filter(responsavel=funcionario, estado=cancelado, dataresolvido__gte=data_inicio,
                                           dataresolvido__lte=data_fim))

            data_resolvidos.append(p3)
            data_cancelados.append(p4)
            data_aceites.append(p2)

        data = {
            'labels': labels,
            'chart_labels': 'my_data',
            'data_resolvidos': data_resolvidos,
            'data_aceites': data_aceites,
            'data_cancelados': data_cancelados
        }
        return JsonResponse(data)


def pedidos_media(request):
    if not request.user.is_authenticated or not request.user.groups.filter(name="Funcionario").exists():
        return redirect('/requestmanager/welcome/')

    anoletivo = request.GET.get('anoletivo')
    tipo = request.GET.get('tipo')
    first_date = request.GET.get('first_date')
    second_date = request.GET.get('second_date')
    
    anoletivo = AnoLetivo.objects.get(nome=anoletivo)
    if tipo == "Todos":
        tipo = "Todos"
    else:
        tipo = TipoPedido.objects.get(nome=tipo)


    estado = EstadoPedido.objects.get(pk=3)

    if first_date == '' or second_date == '':
        if tipo == "Todos":
            pedidos = Pedido.objects.filter(anoletivo = anoletivo, estado=estado)
        else:
            pedidos = Pedido.objects.filter(anoletivo= anoletivo, tipo = tipo, estado=estado)
    else:
        data_inicio = datetime.strptime(first_date, '%Y-%m-%d').date().isoformat()
        data_fim = datetime.strptime(second_date, '%Y-%m-%d').date().isoformat()
        if tipo == "Todos":
            pedidos = Pedido.objects.filter(anoletivo = anoletivo, estado=estado, dataresolvido__gte=data_inicio,
                                            dataresolvido__lte=data_fim)
        else:
            pedidos = Pedido.objects.filter(anoletivo= anoletivo, tipo = tipo, estado=estado, dataresolvido__gte=data_inicio,
                                            dataresolvido__lte=data_fim)


    media = get_media(pedidos)
    
    if (media == 0):
        return JsonResponse(str(0), safe=False)

    days = math.floor(media / (24*60))
    leftover_minutes = media % (24*60)
    hours = math.floor(leftover_minutes / 60)
    mins = math.floor(media - (days*1440) - (hours*60))
    if(days == 1):
        time = f'{days} dia, {hours}h:{mins}m'
    else:
        time = f'{days} dias, {hours}h:{mins}m'


    return JsonResponse(time, safe=False)


# DAR PARSE DE DAYS
def get_media(pedidos):
    soma = 0
    for pedido in pedidos:
        dateString = pedido.tempoprocesso
        check = True
        index = pedido.tempoprocesso.find("days")
        if (index == -1 ):
            index = pedido.tempoprocesso.find("day")
            check = False
        print("asdasdasdasdasdads")
        print (index)
        total_min = 0
        if (index != -1):
            days = int(pedido.tempoprocesso[0:index])
            if (check):
                dateString = pedido.tempoprocesso[index + 6:len(pedido.tempoprocesso)]
            else: 
                dateString = pedido.tempoprocesso[index + 5:len(pedido.tempoprocesso)]
            total_min += days * 24 * 60
        datet = datetime.strptime(dateString, '%H:%M:%S.%f')
        total_min += datet.hour * 60 + datet.minute
        soma += total_min
    if len(pedidos) == 0:
        return 0
    return soma / len(pedidos)


alChoices = list(AnoLetivo.objects.all())
tipos = list(TipoPedido.objects.all())


class chart(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/requestmanager/welcome/')
        return render(request, 'statmanager/chart_pedidos.html', {'tipos': tipos, 'alChoices': alChoices})


class chartPedidos(APIView):

    def get(self, request, format=None):
        labels = [
            'Outros',
            'SALAS',
            'UC',
            'Horarios'
        ]
        chartLabel = "my data"

        pendente = EstadoPedido.objects.get(pk=1)
        aceite = EstadoPedido.objects.get(pk=2)
        resolvido = EstadoPedido.objects.get(pk=3)

        n_pdd_outros = len(list(Pedido.objects.filter(tipo=1)))
        n_pdd_salas = len(list(Pedido.objects.filter(tipo=2)))
        n_pdd_uc = len(list(Pedido.objects.filter(tipo=3)))
        n_pdd_hora = len(list(Pedido.objects.filter(tipo=4)))

        pedidos_pedentes = Pedido.objects.filter(estado=pendente)
        pedidos_aceites = Pedido.objects.filter(estado=aceite)
        pedidos_resolvidos = Pedido.objects.filter(estado=resolvido)

        pedidosOutros_pedentes = len(list(Pedido.objects.filter(estado=pendente, tipo=1)))
        pedidosOutros_aceites = len(list(Pedido.objects.filter(estado=aceite, tipo=1)))
        pedidosOutros_resolvidos = len(list(Pedido.objects.filter(estado=resolvido, tipo=1)))

        pedidosSalas_pedentes = len(list(Pedido.objects.filter(estado=pendente, tipo=2)))
        pedidosSalas_aceites = len(list(Pedido.objects.filter(estado=aceite, tipo=2)))
        pedidosSalas_resolvidos = len(list(Pedido.objects.filter(estado=resolvido, tipo=2)))

        pedidosUcs_pedentes = len(list(Pedido.objects.filter(estado=pendente, tipo=3)))
        pedidosUcs_aceites = len(list(Pedido.objects.filter(estado=aceite, tipo=3)))
        pedidosUcs_resolvidos = len(list(Pedido.objects.filter(estado=resolvido, tipo=4)))

        pedidosHorarios_pedentes = len(list(Pedido.objects.filter(estado=pendente, tipo=4)))
        pedidosHorarios_aceites = len(list(Pedido.objects.filter(estado=aceite, tipo=4)))
        pedidosHorarios_resolvidos = len(list(Pedido.objects.filter(estado=resolvido, tipo=4)))

        chartdata = [n_pdd_outros, n_pdd_salas, n_pdd_uc, n_pdd_hora]
        chartdata_pendentes = [pedidosOutros_pedentes, pedidosSalas_pedentes, pedidosUcs_pedentes,
                               pedidosHorarios_pedentes]
        chartdata_aceites = [pedidosOutros_aceites, pedidosSalas_aceites, pedidosUcs_aceites, pedidosHorarios_aceites]
        chartdata_resolvidos = [pedidosOutros_resolvidos, pedidosSalas_resolvidos, pedidosUcs_resolvidos,
                                pedidosHorarios_resolvidos]

        data = {
            "labels": labels,
            "chartLabel": chartLabel,
            "chartdata": chartdata,
            "chartdata_pendentes": chartdata_pendentes,
            "chartdata_aceites": chartdata_aceites,
            "chartdata_resolvidos": chartdata_resolvidos
        }
        return Response(data)


MESES = ["JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO", "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO",
         "NOVEMBRO", "DEZEMBRO"]


def getLineChartData(request):
    if not request.user.is_authenticated or not request.user.groups.filter(name="Funcionario").exists():
        return redirect('/requestmanager/welcome/')

    return startupChart(selectanoletivo())


def getLineChartAfterCheck(request):
    if not request.user.is_authenticated or not request.user.groups.filter(name="Funcionario").exists():
        return redirect('/requestmanager/welcome/')

    if request.method == 'GET':
        anoletivo = request.GET.get('anoletivo')
        anoletivo = AnoLetivo.objects.get(nome=anoletivo)
    return startupChart(anoletivo)


def startupChart(anoletivo):
    num_pdd_criados = []
    num_pdd_resolvidos = []
    labels = []
    color1 = []
    color2 = []

    start = anoletivo.datainicio.month
    end = anoletivo.datafim.month

    year1 = anoletivo.datainicio.year
    year2 = anoletivo.datafim.year

    checky1 = year1
    checky2 = year2

    switch = False
    while (start < end or checky1 < checky2):
        if (anoletivo.datafim.year > anoletivo.datainicio.year and start == 12):
            start = 0
            checky1 += 1
            switch = True
        if (switch):
            num1 = len(Pedido.objects.filter(datacriacao__month=start, datacriacao__year=year2))
            num2 = len(Pedido.objects.filter(dataresolvido__month=start, datacriacao__year=year2))
        else:
            num1 = len(Pedido.objects.filter(datacriacao__month=start, datacriacao__year=year1))
            num2 = len(Pedido.objects.filter(dataresolvido__month=start, datacriacao__year=year1))
        num_pdd_criados.append(num1)
        num_pdd_resolvidos.append(num2)
        color1.append('rgba(255, 99, 132, 0.5)')
        color2.append('rgba(54, 162, 235, 0.5)')
        labels.append(MESES[start])

        start += 1

    chartLabel = ["Pedidos Criados", "Pedidos Resolvidos"]

    chartdata = [num_pdd_criados, num_pdd_resolvidos]
    data = {
        "labels": labels,
        "chartLabel": chartLabel,
        "chartdata": chartdata,
        "color1": color1,
        "color2": color2
    }
    print(num_pdd_criados)
    print(num_pdd_resolvidos)

    return JsonResponse(data)
