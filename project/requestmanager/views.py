import datetime
import math
from django.http import HttpResponseRedirect

from django.shortcuts import render, redirect
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from .filters import *
from .forms import *
from .tables import *
from .models import *

from django.contrib.auth.models import Group
from django.contrib import messages


#################################################
##### Ordem:                                #####
#####      -Pedido de Unidade Curricular    #####
#####      -Pedido de Sala de Aula          #####
#####      -Pedido de Horários              #####
#####      -Pedido Outros                   #####
#####      -List                            #####
#####      -App Render                      #####
#################################################

def selectanoletivo():
    today = date.today()
    anoletivo = AnoLetivo.objects.filter(datainicio__lte=today, datafim__gte=today)
    return anoletivo[0]


#################################################################################
##### PEDIDO UNIDADE CURRICULAR #################################################
##### Autor: André Oliveira     #################################################
#################################################################################

# TODO - VERIFICAR SE NAO HA COISAS VAZIAS

# CREATE
def create_unidadeCurricular(request):
    if not request.user.is_authenticated or not request.user.groups.filter(name='ProfessorUniversitario').exists():
        return redirect('/requestmanager/welcome/')
    #
    import datetime
    min_date = (datetime.datetime.today()).date().isoformat()
    max_date = selectanoletivo().datafim.isoformat()

    if request.method == 'POST':
        formpedido = PedidoForm(request.POST)
        # if formpedido.is_valid():
        assunto = request.POST.get('assunto')
        descricao = request.POST.get('descricao')
        data = request.POST.get('data')

        if assunto.strip() == "" or descricao.strip() == "" or data == "":
            errors = "Todos os campos devem ser preenchidos."
            return render(request, 'requestmanager/create_unidadecurricular.html',
                          {'form': formpedido, 'errors': errors, 'min_date': min_date, 'max_date': max_date})

        ##### ERROR CHECKING ###
        # date_1 = datetime.strptime(data, "%Y-%m-%d")
        # today_date = datetime.strptime(str(datetime.today()).split(' ')[0], "%Y-%m-%d")
        # if date_1 < today_date or date_1 > datetime.strptime(str(selectanoletivo().datafim).split(' ')[0],
        #                                                      "%Y-%m-%d"):
        #     errors = "A data-alvo selecionada deve estar entre o dia atual e a data final do ano letivo atual."
        #     # errors = "A data-alvo selecionada deve ser a do pedido mais próximo da data atual."
        #     return render(request, 'requestmanager/create_unidadecurricular.html',
        #                   {'formpedido': formpedido, 'errors': errors, 'min_date': min_date, 'max_date': max_date})
        docente = ProfessorUniversitario.objects.get(pk=request.user.id)

        pedido = Pedido(docente=docente, assunto=assunto, descricao=descricao, dataalvo=data,
                        estado_id=1, tipo=TipoPedido.objects.get(pk=3), anoletivo=selectanoletivo())

        objects = []
        size = math.ceil(((len(list(request.POST.dict()))) - 4) / 5)
        for i in range(0, size):
            acao_pedido = request.POST["acao" + str(i)]
            turma_pedido = request.POST['turma' + str(i)]
            unidade_pedido = request.POST['unidade' + str(i)]
            assunto_pedido = request.POST['assunto' + str(i)]
            pedido_uc = Pedidouc(acao=Acao.objects.get(pk=acao_pedido),
                                 tipoturmaid=TipoTurma.objects.get(pk=turma_pedido),
                                 unidadecurricularid_id=unidade_pedido, assunto=assunto_pedido,
                                 pedido_ptr_id=pedido)
            objects.append(pedido_uc)

        pedido.save()
        for p in objects:
            p.save()

        messages.info(request, 'Pedido criado com sucesso')
        return redirect('/requestmanager/app/' + str(request.user.id))
    else:
        formpedido = PedidoForm()
        return render(request, 'requestmanager/create_unidadecurricular.html',
                      {'form': formpedido, 'min_date': min_date, 'max_date': max_date})


# EDIT
def edit_unidadeCurricular(request, pedidoID):
    if not request.user.is_authenticated or not request.user.groups.filter(name='ProfessorUniversitario').exists():
        return redirect('/requestmanager/welcome/')

    if not request.user.is_authenticated:
        return redirect('/requestmanager/welcome/')
    #
    import datetime
    min_date = (datetime.datetime.today()).date().isoformat()
    max_date = selectanoletivo().datafim.isoformat()

    pedido = Pedido.objects.get(id=pedidoID)
    pedidouc = Pedidouc.objects.filter(pedido_ptr_id_id=pedidoID)
    error_data = False
    if request.method == 'POST':
        form = edit_unidadesCurriculares(request.POST)
        if form.is_valid():
            descricao = request.POST.get('descricao')
            assunto = request.POST.get('assunto')
            data = request.POST.get('data')

            pedido.descricao = descricao
            pedido.assunto = assunto
            pedido.dataalvo = data

            ids_atualizados = []  # Guarda quais os ids dos pedidodinhos que foram alterados e criados
            objects = []
            size = math.ceil(((len(list(request.POST.dict()))) - 4) / 5)
            for i in range(0, size):
                acao_pedido = request.POST["acao" + str(i)]
                turma_pedido = request.POST['turma' + str(i)]
                unidade_pedido = request.POST['unidade' + str(i)]
                assunto_pedido = request.POST['assunto' + str(i)]

                if acao_pedido.strip() == "" or turma_pedido.strip() == "" or unidade_pedido == "" or assunto_pedido == "":
                    errors = "Todos os campos devem ser preenchidos."
                    return render(request, 'requestmanager/edit_unidadecurricular.html',
                                  {'form': form, 'errors': errors, 'min_date': min_date, 'max_date': max_date})

                # Se nao há mais pedidodinho, significa que é um pedidodinho novo retornando o ultimo id da tabela + 1
                try:
                    ultimo_pedido_uc = Pedidouc.objects.last().id + 1
                except:
                    ultimo_pedido_uc = 1

                last_pedidodinho = request.POST.get("pedidodinho" + str(i), ultimo_pedido_uc)
                ids_atualizados.append(str(last_pedidodinho))

                old_pedidouc, iscreated = Pedidouc.objects.get_or_create(id=last_pedidodinho)
                old_pedidouc.unidadecurricularid = Unidadecurricular.objects.get(id=unidade_pedido)
                old_pedidouc.acao = Acao.objects.get(id=acao_pedido)
                old_pedidouc.tipoturmaid = TipoTurma.objects.get(pk=turma_pedido)
                old_pedidouc.assunto = assunto_pedido
                old_pedidouc.pedido_ptr_id = pedido
                objects.append(old_pedidouc)

            pedido.save()

            for p in objects:
                p.save()

            for pedido in pedidouc:
                if str(pedido.id) not in ids_atualizados:
                    pedido.delete()
            messages.info(request, 'Pedido editado com sucesso')
            return redirect('/requestmanager/app/' + str(request.user.id))
        return render(request, 'requestmanager/consult_unidadecurricular.html',
                      {'id': pedidoID, 'min_date': min_date, 'max_date': max_date})

    else:
        form = PedidoForm(initial={'assunto': pedido.assunto, 'descricao': pedido.descricao, 'data': pedido.dataalvo})
    context = {
        'form': form, 'min_date': min_date, 'max_date': max_date
    }
    return render(request, 'requestmanager/edit_unidadecurricular.html', context)


# DELETE
def delete_unidadeCurricular(request, pedidoID):
    if not request.user.is_authenticated or not request.user.groups.filter(name='ProfessorUniversitario').exists():
        return redirect('/requestmanager/welcome/')

    if not request.user.is_authenticated:
        return redirect('/requestmanager/welcome/')

    if request.method == 'POST':
        form = delete_unidadesCurriculares(request.POST)
        if form.is_valid():
            pedidouc = Pedidouc.objects.get(pk=pedidoID)
            id = request.POST.get('id')
            pedidouc.delete()
            print("apagado")
    else:
        form = delete_unidadesCurriculares()

    context = {
        'form': form,
        'list': list(Pedidouc.objects.raw(
            'SELECT * FROM Pedidouc LEFT JOIN Unidadecurricular ON Pedidouc.unidadecurricularid = Unidadecurricular.id'))
    }
    return render(request, 'requestmanager/delete_unidadecurricular.html', context)


# CONSULT
def consult_unidadeCurricular(request, id):
    if not request.user.is_authenticated:
        return redirect('/requestmanager/welcome/')

    pedido = Pedido.objects.get(id=id)
    form = PedidoForm(initial={'assunto': pedido.assunto, 'descricao': pedido.descricao, 'data': pedido.dataalvo})
    state = pedido.estado
    pendente = EstadoPedido.objects.get(pk=1)
    resolvido = EstadoPedido.objects.get(pk=3)
    context = {
        'id': id,
        'form': form,
        'change': state == pendente

    }
    return render(request, 'requestmanager/consult_unidadecurricular.html', context)


##########################################################################################
######### PEDIDO SALA DE AULA      #######################################################
######### Autor: António Madureira #######################################################
##########################################################################################

# CREATE
def create_pedidoSala(request):
    if not request.user.is_authenticated or not request.user.groups.filter(name='ProfessorUniversitario').exists():
        return redirect('/requestmanager/welcome/')

    if not request.user.is_authenticated:
        return redirect('/requestmanager/welcome/')
    #
    import datetime
    min_date = (datetime.datetime.today()).date().isoformat()
    max_date = selectanoletivo().datafim.isoformat()

    if request.method == 'POST':
        form = pedidoForm(request.POST)
        formset = formset_sala(request.POST)
        if form.is_valid():
            descricao = form.cleaned_data['descricao']
            assunto = form.cleaned_data['assunto']
            data = str(form.cleaned_data['data'])
            tipo_pedido = TipoPedido.objects.get(pk=2)
            estado = EstadoPedido.objects.get(pk=1)

            docent = ProfessorUniversitario.objects.get(pk=request.user.id)

            new_pedido = Pedido(descricao=descricao, assunto=assunto, tipo=tipo_pedido, estado=estado, dataalvo=data,
                                anoletivo=selectanoletivo(), docente_id=request.user.id)

            objects = []
            size = math.ceil(((len(list(request.POST.dict()))) - 4) / 7)
            for i in range(0, size):
                lotacao_pedido = request.POST['lotacao' + str(i)]
                data_pedido = request.POST['data' + str(i)]
                hora_inicio = request.POST['horainicio' + str(i)]
                hora_fim = request.POST['horafim' + str(i)]
                id_acao = request.POST["acao" + str(i)]
                id_tipo = request.POST['tipos' + str(i)]
                id_cs = request.POST['tiposala' + str(i)]

                ##### ERROR CHECKING ###
                if id_acao.strip() == "" or lotacao_pedido.strip() == "" or data_pedido == "" or hora_inicio == "" or hora_fim == "" or id_tipo == "" or id_cs == "":
                    errors = "Todos os campos devem ser preenchidos."
                    return render(request, 'requestmanager/create_pedidoSala.html',
                                  {'pedidoSalaForm': form, 'errors': errors, 'min_date': min_date,
                                   'max_date': max_date})
                # else:
                #     date_1 = datetime.strptime(data_pedido, "%Y-%m-%d")
                #     today_date = datetime.strptime(str(datetime.today()).split(' ')[0], "%Y-%m-%d")
                #     if date_1 < today_date or date_1 > datetime.strptime(str(selectanoletivo().datafim).split(' ')[0],
                #                                                          "%Y-%m-%d"):
                #         errors = "A data-alvo de uma alínea selecionada deve estar entre o dia atual e a data final do ano letivo atual."
                #         # errors = "A data-alvo selecionada deve ser a do pedido mais próximo da data atual."
                #         return render(request, 'requestmanager/create_pedidoSala.html',
                #                       {'formpedido': form, 'errors': errors, 'min_date': min_date,
                #                        'max_date': max_date})
                
                acao_pedido = Acao.objects.get(id=id_acao)
                tipo = Tipopedidosala.objects.get(id=id_tipo)
                cs = Categoriasala.objects.get(id=id_cs)
                pedido_sala = Pedidosala(acao=acao_pedido, data=data_pedido, alunosprevistos=lotacao_pedido,
                                         horainicio=hora_inicio,
                                         horafim=hora_fim, tipopedidosalaid=tipo, categoriasalaid=cs,
                                         pedido_ptr_id=new_pedido)
                objects.append(pedido_sala)

            new_pedido.save()
            for p in objects:
                p.save()

            messages.info(request, 'Pedido criado com sucesso')
            return redirect('/requestmanager/app/' + str(request.user.id))
        else:
            print(form.errors.as_data())
    else:
        form = pedidoForm()
        formset = formset_sala()
    return render(request, 'requestmanager/create_pedidoSala.html',
                  {'pedidoSalaForm': form, 'formset': formset, 'min_date': min_date, 'max_date': max_date})


# EDIT
def edit_pedidoSala(request, pedidoID):
    if not request.user.is_authenticated or not request.user.groups.filter(name='ProfessorUniversitario').exists():
        return redirect('/requestmanager/welcome/')

    if not request.user.is_authenticated:
        return redirect('/requestmanager/welcome/')
    #
    import datetime
    min_date = (datetime.datetime.today()).date().isoformat()
    max_date = selectanoletivo().datafim.isoformat()
    big_pedido = Pedido.objects.get(pk=pedidoID)  # Pedido principal
    pedidossala = Pedidosala.objects.filter(pedido_ptr_id_id=pedidoID)
    error_data = False
    if request.method == 'POST':
        form = pedidoSalaEditForm(request.POST)
        if form.is_valid():
            # Obter dados do post request e guardar atualizar o objeto big_pedido.
            assunto = request.POST.get('assunto')
            descricao = request.POST.get('descricao')
            data = request.POST.get('data')
            big_pedido.assunto = assunto
            big_pedido.descricao = descricao
            big_pedido.dataalvo = data

            ##### ERROR CHECKING ###
            # date_1 = datetime.strptime(data, "%Y-%m-%d")
            # today_date = datetime.strptime(str(datetime.today()).split(' ')[0], "%Y-%m-%d")
            # if date_1 < today_date or date_1 > datetime.strptime(str(selectanoletivo().datafim).split(' ')[0],
            #                                                      "%Y-%m-%d"):
            #     errors = "A data-alvo selecionada deve estar entre o dia atual e a data final do ano letivo atual."
            #     # errors = "A data-alvo selecionada deve ser a do pedido mais próximo da data atual."
            #     return render(request, 'requestmanager/edit_pedidoSala.html',
            #                   {'pedidoSalaForm': form, 'errors': errors, 'min_date': min_date,
            #                    'max_date': max_date})

            ids_atualizados = []  # Guarda quais os ids dos pedidodinhos que foram alterados e criados
            size = int(((len(list(request.POST.dict()))) - 4) / 7)

            objects = []
            # Atualiza ou cria pedidodinhos
            for i in range(0, size):
                lotacao_pedido = request.POST['lotacao' + str(i)]
                data_pedido = request.POST['data' + str(i)]
                hora_inicio = request.POST['horainicio' + str(i)]
                hora_fim = request.POST['horafim' + str(i)]
                id_acao = request.POST["acao" + str(i)]
                id_tipo = request.POST['tipos' + str(i)]
                id_cs = request.POST['tiposala' + str(i)]

                # cs = Categoriasala.objects.get(id=id_cs)
                # Se nao há mais pedidodinho, significa que é um pedidodinho novo retornando o ultimo id da tabela + 1
                try:
                    ultimo_pedido_sala = Pedidosala.objects.last().id + 1
                except:
                    ultimo_pedido_sala = 1
                last_pedidodinho = request.POST.get("pedidodinho" + str(i), ultimo_pedido_sala)
                ids_atualizados.append(str(last_pedidodinho))

                ##### ERROR CHECKING ###
                if id_acao.strip() == "" or lotacao_pedido.strip() == "" or data_pedido == "" or hora_inicio == "" or hora_fim == "" or id_tipo == "" or id_cs == "":
                    errors = "Todos os campos devem ser preenchidos."
                    return render(request, 'requestmanager/edit_pedidoSala.html',
                                  {'pedidoSalaForm': form, 'errors': errors, 'min_date': min_date,
                                   'max_date': max_date})
                # else:
                #     date_1 = datetime.strptime(data_pedido, "%Y-%m-%d")
                #     today_date = datetime.strptime(str(datetime.today()).split(' ')[0], "%Y-%m-%d")
                #     if date_1 < today_date or date_1 > datetime.strptime(str(selectanoletivo().datafim).split(' ')[0],
                #                                                          "%Y-%m-%d"):
                #         errors = "A data-alvo selecionada deve estar entre o dia atual e a data final do ano letivo atual."
                #         # errors = "A data-alvo selecionada deve ser a do pedido mais próximo da data atual."
                #         return render(request, 'requestmanager/edit_pedidoSala.html',
                #                       {'pedidoSalaForm': form, 'errors': errors, 'min_date': min_date,
                #                        'max_date': max_date})

                acao_pedido = Acao.objects.get(id=id_acao)
                tipo = Tipopedidosala.objects.get(id=id_tipo)
                cs = Categoriasala.objects.get(id=id_cs)

                old_pedidosala, iscreated = Pedidosala.objects.get_or_create(id=last_pedidodinho)
                old_pedidosala.alunosprevistos = lotacao_pedido
                old_pedidosala.data = data_pedido
                old_pedidosala.horainicio = hora_inicio
                old_pedidosala.horafim = hora_fim
                old_pedidosala.tipopedidosalaid = tipo
                old_pedidosala.categoriasalaid = cs
                old_pedidosala.pedido_ptr_id = big_pedido
                old_pedidosala.acao = acao_pedido

                objects.append(old_pedidosala)

            big_pedido.save()
            for p in objects:
                p.save()

            '''Verificar pedidodinhos removidos'''
            # Pega nos pedidosoutros que estao ligado ao pedido principal
            # e verifica quais os que foram mandados no request
            # e elimina os que estão ligados ao pedido mas nao estao no request
            for pedido in pedidossala:
                if str(pedido.id) not in ids_atualizados:
                    pedido.delete()

            # return sucesso_view(request, 'O pedido foi editado com sucesso!')

            messages.info(request, 'Pedido editado com sucesso')
            return redirect('/requestmanager/app/' + str(request.user.id))

        else:
            print(form.errors.as_data)
    else:
        form = pedidoSalaEditForm(initial={'assunto': big_pedido.assunto,
                                           'descricao': big_pedido.descricao,
                                           'data': big_pedido.dataalvo})
    return render(request, 'requestmanager/edit_pedidoSala.html',
                  {'pedidoSalaForm': form, 'min_date': min_date, 'max_date': max_date})


# DELETE
def delete_pedidoSala(request):
    if not request.user.is_authenticated:
        return redirect('/requestmanager/welcome/')

    if request.method == 'POST':
        form = pedidoSalaDeleteForm(request.POST)
        if form.is_valid():
            id = request.POST.get('id')
            pedidoSala = Pedidosala.objects.get(pk=id)
            pedidoSala.delete()
        else:
            print(form.errors.as_data())
    else:
        print("ERRO")
        form = pedidoSalaDeleteForm()
    return render(request, 'requestmanager/delete_pedidoSala.html',
                  {'pedidoSalaDeleteForm': form, 'list': list(Pedidosala.objects.all())})


# CONSULT
def consult_pedidoSala(request, pedidoID):
    if not request.user.is_authenticated:
        return redirect('/requestmanager/welcome/')

    pedido = Pedido.objects.get(pk=pedidoID)
    context = {
        "id": pedidoID,
        'pendente': pedido.anoletivo == selectanoletivo() and pedido.estado_id == 1,
        'resolvido': pedido.anoletivo == selectanoletivo() and pedido.estado_id != 3 and pedido.estado_id == 2,
    }
    return render(request, 'requestmanager/consult_pedidosala.html', context)


###################################################################################
######### PEDIDO HORARIOS   #######################################################
######### Autor: Tomás Roma #######################################################
###################################################################################

# TODO: FAZER VERIFICAO DOS ANOS LETIVOS

# CREATE
def create_pedidoHorario(request):
    if not request.user.is_authenticated or not request.user.groups.filter(name='ProfessorUniversitario').exists():
        return redirect('/requestmanager/welcome/')

    import datetime
    min_date = (datetime.datetime.today()).date().isoformat()
    max_date = selectanoletivo().datafim.isoformat()

    if request.method == 'POST':
        form = pedidoForm(request.POST, request.FILES)
        # if form.is_valid():
        descricao = request.POST["descricao"]
        data = request.POST["data"]
        assunto = request.POST["assunto"]
        today = date.today()
        pedidoestado = EstadoPedido.objects.get(pk=1)
        anoletivo = selectanoletivo()
        tipo_pedido = TipoPedido.objects.get(pk=4)

        docente = ProfessorUniversitario.objects.get(pk=request.user.id)

        new_pedido = Pedido(docente_id=request.user.id, tipo=tipo_pedido, estado=pedidoestado, descricao=descricao,
                            dataalvo=data, anoletivo=anoletivo, assunto=assunto)

        objects = []
        size = math.ceil(((len(list(request.POST.dict()))) - 4) / 8)
        # print(size)
        for i in range(0, size):
            descricao_pedido = request.POST['descricao' + str(i)]
            dataorigem_pedido = request.POST['data_origem' + str(i)]
            horaorigem_pedido = request.POST['hora_origem' + str(i)]
            datamudanca_pedido = request.POST['data_mudanca' + str(i)]
            horamudanca_pedido = request.POST['hora_mudanca' + str(i)]
            id_tipoacao = request.POST['acao' + str(i)]
            id_tipo_alteracao = request.POST['alteracao_pdd' + str(i)]

            ##### ERROR CHECKING ###
            if dataorigem_pedido.strip() == "" or descricao_pedido.strip() == "" or horaorigem_pedido == "" or id_tipoacao == "" or id_tipo_alteracao == "":
                errors = "Todos os campos devem ser preenchidos."
                return render(request, 'requestmanager/create_pedidoHorario.html',
                              {'form': form, 'errors': errors, 'min_date': min_date,
                               'max_date': max_date})

            # tipo_pedido = Tipopedidohorario.objects.get(nome=id_tipo)
            tipo_pedidoacao = Acao.objects.get(pk=id_tipoacao)
            # print(id_tipoacao)
            tipo_alt = Tipoalteracaohorario.objects.get(nome=id_tipo_alteracao)
            pedido_horario = Pedidohorario(descricao=descricao_pedido, dataorigem=dataorigem_pedido,
                                           datamudanca=datamudanca_pedido,
                                           acao=tipo_pedidoacao, tipoalteracaohorarioid=tipo_alt,
                                           horaorigem=horaorigem_pedido,
                                           horamudanca=horamudanca_pedido,
                                           pedido_ptr_id=new_pedido)

            objects.append(pedido_horario)
        new_pedido.save()
        for p in objects:
            p.save()

        messages.info(request, 'Pedido criado com sucesso')
        return redirect('/requestmanager/app/' + str(request.user.id))
    # return sucesso_view(request, 'O pedido foi criado com sucesso!')
    else:
        form = pedidoForm()
        anoletivo = selectanoletivo()
        return render(request, 'requestmanager/create_pedidoHorario.html', {'form': form, 'min_date': min_date,
                                                                            'max_date': max_date})


# EDIT
def edit_pedidoHorario(request, pdd_id):
    if not request.user.is_authenticated or not request.user.groups.filter(name='ProfessorUniversitario').exists():
        return redirect('/requestmanager/welcome/')
    #
    import datetime
    min_date = (datetime.datetime.today()).date().isoformat()
    max_date = selectanoletivo().datafim.isoformat()

    pedido_original = Pedido.objects.get(pk=pdd_id)
    pedidos_horario = Pedidohorario.objects.filter(pedido_ptr_id=pdd_id)
    if request.method == 'POST':
        descricao_edit = request.POST.get("descricao")
        data_edit = request.POST.get("data")
        assunto_edit = request.POST.get("assunto")
        pedido_original.descricao = descricao_edit
        pedido_original.dataalvo = data_edit
        pedido_original.assunto = assunto_edit

        ##### ERROR CHECKING ###
        # date_1 = datetime.strptime(data_edit, "%Y-%m-%d")
        # today_date = datetime.strptime(str(datetime.today()).split(' ')[0], "%Y-%m-%d")
        # if date_1 < today_date or date_1 > datetime.strptime(str(selectanoletivo().datafim).split(' ')[0],
        #                                                      "%Y-%m-%d"):
        #     errors = "A data de mudança selecionada deve estar entre o dia atual e a data final do ano letivo atual."
        #     # errors = "A data-alvo selecionada deve ser a do pedido mais próximo da data atual."
        #     return render(request, 'requestmanager/edit_pedidoHorario.html',
        #                   {'errors': errors, 'min_date': min_date,
        #                    'max_date': max_date})

        ids_subPedidos = []
        objects = []
        size = math.ceil(((len(list(request.POST.dict()))) - 4) / 8)
        print(size)
        for i in range(0, size):
            tipoAlteracao_edit = request.POST.get("tipo_alteracao" + str(i))
            dataorigem_edit = request.POST.get("data_origem" + str(i))
            horaorigem_edit = request.POST.get("hora_origem" + str(i))
            datamudanca_edit = request.POST.get("data_mudanca" + str(i))
            horamudanca_edit = request.POST.get("hora_mudanca" + str(i))
            subdescricao = request.POST.get("descricao" + str(i))
            id_acao = request.POST["acao" + str(i)]

            ##### ERROR CHECKING ###
            if id_acao.strip() == "" or tipoAlteracao_edit.strip() == "" or dataorigem_edit == "" or horaorigem_edit == "" or datamudanca_edit == "" or horamudanca_edit == "" or subdescricao == "":
                errors = "Todos os campos devem ser preenchidos."
                return render(request, 'requestmanager/edit_pedidoHorario.html',
                              {'errors': errors, 'min_date': min_date,
                               'max_date': max_date})
            # else:
            #     date_1 = datetime.strptime(datamudanca_edit, "%Y-%m-%d")
            #     today_date = datetime.strptime(str(datetime.today()).split(' ')[0], "%Y-%m-%d")
            #     if date_1 < today_date or date_1 > datetime.strptime(str(selectanoletivo().datafim).split(' ')[0],
            #                                                          "%Y-%m-%d"):
            #         errors = "A data de mudança selecionada deve estar entre o dia atual e a data final do ano letivo atual."
            #         return render(request, 'requestmanager/edit_pedidoHorario.html',
            #                       {'errors': errors, 'min_date': min_date,
            #                        'max_date': max_date})

            try:
                ultimo_pedido_horario = Pedidohorario.objects.last().id + 1
            except:
                ultimo_pedido_horario = 1
            last_pedidodinho = request.POST.get("pedidodinho" + str(i), ultimo_pedido_horario)
            ids_subPedidos.append(str(last_pedidodinho))

            # print(tipoAlteracao_edit)
            # print(last_pedidodinho)
            acao_pedido = Acao.objects.get(id=id_acao)

            pedidoHora, iscreated = Pedidohorario.objects.get_or_create(id=last_pedidodinho)
            pedidoHora.pedido_ptr_id = pedido_original
            pedidoHora.descricao = subdescricao
            pedidoHora.tipoalteracaohorarioid = Tipoalteracaohorario.objects.get(nome=tipoAlteracao_edit)
            pedidoHora.dataorigem = dataorigem_edit
            pedidoHora.horaorigem = horaorigem_edit
            pedidoHora.datamudanca = datamudanca_edit
            pedidoHora.horamudanca = horamudanca_edit
            pedidoHora.acao = acao_pedido
            objects.append(pedidoHora)

        for p in objects:
            p.save()

        for pedido in pedidos_horario:
            if str(pedido.id) not in ids_subPedidos:
                pedido.delete()

        pedido_original.save()

        messages.info(request, 'Pedido editado com sucesso')
        return redirect('/requestmanager/app/' + str(request.user.id))
    return render(request, 'requestmanager/edit_pedidoHorario.html', {'min_date': min_date,
                                                                      'max_date': max_date})


def consult_pedidoHorario(request, pdd_id):
    if not request.user.is_authenticated or not request.user.groups.filter(name='ProfessorUniversitario').exists():
        return redirect('/requestmanager/welcome/')

    pedido = Pedido.objects.get(pk=pdd_id)
    context = {
        "id": pdd_id,
        "change": True,
        'pendente': pedido.anoletivo == selectanoletivo() and pedido.estado_id == 1,
        'resolvido': pedido.anoletivo == selectanoletivo() and pedido.estado_id != 3 and pedido.estado_id == 2,
    }
    return render(request, 'requestmanager/consult_pedidoHorario.html', context)


########################################################################################
######## PEDIDO OUTROS          ########################################################
######## Autor: Gonçalo Almeida ########################################################
########################################################################################

# CREATE
def create_pedidooutro(request):
    if not request.user.is_authenticated or not request.user.groups.filter(name='ProfessorUniversitario').exists():
        return redirect('/requestmanager/welcome/')
    #
    import datetime
    min_date = (datetime.datetime.today()).date().isoformat()
    max_date = selectanoletivo().datafim.isoformat()

    errors = ""
    if request.method == 'POST':
        old_data = {}
        for key in request.POST:
            old_data[key] = request.POST.get(key)
        # print(old_data["data"])

        formpedido = PedidoForm(request.POST)
        assunto = formpedido.data.get('assunto')
        descricao = formpedido.data.get('descricao')
        data = formpedido.data.get('date')

        ##### ERROR CHECKING ###
        # date_1 = datetime.strptime(data, "%Y-%m-%d")
        # today_date = datetime.strptime(str(datetime.today()).split(' ')[0], "%Y-%m-%d")
        # if date_1 < today_date or date_1 > datetime.strptime(str(selectanoletivo().datafim).split(' ')[0],
        #                                                      "%Y-%m-%d"):
        #     errors = "A data-alvo selecionada deve estar entre o dia atual e a data final do ano letivo atual."
        #     # errors = "A data-alvo selecionada deve ser a do pedido mais próximo da data atual."
        #     return render(request, 'requestmanager/create_outrosform.html',
        #                   {'formpedido': formpedido, 'errors': errors, 'old_data': old_data, 'min_date': min_date,
        #                    'max_date': max_date})

        pedido = Pedido(assunto=assunto, descricao=descricao, dataalvo=data,
                        estado_id=1, tipo=TipoPedido.objects.get(pk=1), anoletivo=selectanoletivo(),
                        docente_id=request.user.id)

        size = math.ceil(((len(list(request.POST.dict()))) - 4) / 3)
        objects = []
        for i in range(0, size):
            assunto_pedido = request.POST["assunto" + str(i)]
            descricao_pedido = request.POST['descricao' + str(i)]
            data_pedido = request.POST['date' + str(i)]

            if assunto_pedido.strip() == "" or descricao_pedido.strip() == "" or data_pedido == "":
                errors = "Todos os campos devem ser preenchidos."
                return render(request, 'requestmanager/create_outrosform.html',
                              {'formpedido': formpedido, 'errors': errors, 'old_data': old_data,
                               'min_date': min_date,
                               'max_date': max_date})
            # else:
            #     date_1 = datetime.strptime(data_pedido, "%Y-%m-%d")
            #     if date_1 < datetime.strptime(str(datetime.today()).split(' ')[0], "%Y-%m-%d"):
            #         errors = "A data-alvo selecionada deve ser para depois do dia atual."
            #         return render(request, 'requestmanager/create_outrosform.html',
            #                       {'formpedido': formpedido, 'errors': errors, 'min_date': min_date,
            #                        'max_date': max_date})

            pedido_outro = Pedidooutros(assunto_pedido=assunto_pedido, descricao_pedido=descricao_pedido,
                                        dataalvo_pedido=data_pedido, pedido_ptr_id=pedido)
            objects.append(pedido_outro)

        ##### IF NO ERRORS SAVE ALL
        pedido.save()
        for p in objects:
            p.save()
        messages.info(request, 'Pedido criado com sucesso')
        return redirect('/requestmanager/app/' + str(request.user.id))
    # else:
    #     errors = "Todos os campos devem ser preenchidos."
    #     return render(request, 'requestmanager/create_outrosform.html',
    #                   {'formpedido': formpedido, 'errors': errors, 'old_data': old_data, 'min_date': min_date,
    #                    'max_date': max_date})
    formpedido = PedidoForm()

    context = {'formpedido': formpedido,
               'errors': errors,
               'min_date': min_date,
               'max_date': max_date
               }
    return render(request, 'requestmanager/create_outrosform.html',
                  {'formpedido': formpedido, 'errors': errors, 'min_date': min_date,
                   'max_date': max_date})


# EDIT
def edit_pedidooutro(request, pdd_id):
    if not request.user.is_authenticated or not request.user.groups.filter(name='ProfessorUniversitario').exists():
        return redirect('/requestmanager/welcome/')
    import datetime
    min_date = (datetime.datetime.today()).date().isoformat()
    # # import datetime
    # min_date = (datetime.datetime.today()).date().isoformat()
    max_date = selectanoletivo().datafim.isoformat()

    big_pedido = Pedido.objects.get(pk=pdd_id)  # Pedido principal
    pedidosoutro = Pedidooutros.objects.filter(pedido_ptr_id_id=pdd_id)
    error_data = False
    if request.method == 'POST':
        formpedido = PedidoForm(request.POST)  # Form do pedido principal

        # if formpedido.is_valid():
        print("valid")
        # Obter dados do post request e guardar atualizar o objeto big_pedido.
        descricao = request.POST.get('descricao')
        assunto = request.POST.get('assunto')
        data = request.POST.get('data')

        if assunto.strip() == "" or descricao.strip() == "" or data == "":
            errors = "Todos os campos devem ser preenchidos."
            return render(request, 'requestmanager/edit_outrosform.html',
                          {'formpedido': formpedido, 'errors': errors, 'min_date': min_date,
                           'max_date': max_date})

        ##### ERROR CHECKING ###
        # if str(data) != str(big_pedido.dataalvo):
        #     date_1 = datetime.strptime(data, "%Y-%m-%d")
        #     if date_1 < datetime.today():
        #         errors = "A data-alvo selecionada deve ser para depois do dia atual."
        #         # errors = "A data-alvo selecionada deve ser a do pedido mais próximo da data atual."
        #         return render(request, 'requestmanager/edit_outrosform.html',
        #                       {'formpedido': formpedido, 'errors': errors, 'min_date': min_date,
        #                        'max_date': max_date})
        big_pedido.assunto = assunto
        big_pedido.descricao = descricao
        big_pedido.dataalvo = data

        ids_atualizados = []  # Guarda quais os ids dos pedidodinhos que foram alterados e criados

        size = math.ceil(((len(list(request.POST.dict()))) - 4) / 4)
        objects = []
        print(size)
        # Atualiza ou cria pedidodinhos
        for i in range(0, size):
            assunto_pedido = str(request.POST["assunto" + str(i)])
            descricao_pedido = str(request.POST['descricao' + str(i)])
            data_pedido = str(request.POST['date' + str(i)])

            if assunto_pedido.strip() == "" or descricao_pedido.strip() == "" or data_pedido == "":
                errors = "Todos os campos devem ser preenchidos."
                return render(request, 'requestmanager/edit_outrosform.html',
                              {'formpedido': formpedido, 'errors': errors, 'min_date': min_date,
                               'max_date': max_date})

            # Se nao há mais pedidodinho, significa que é um pedidodinho novo retornando o ultimo id da tabela + 1

            try:
                ultimo_pedido_outro = Pedidooutros.objects.last().id + 1
            except:
                ultimo_pedido_outro = 1
            last_pedidodinho = request.POST.get("pedidodinho" + str(i), ultimo_pedido_outro)
            ids_atualizados.append(str(last_pedidodinho))

            old_pedidooutro, iscreated = Pedidooutros.objects.get_or_create(id=last_pedidodinho)

            # if iscreated:
            #     print("nao existe")
            #     date_1 = datetime.strptime(data_pedido, "%Y-%m-%d")
            #     if date_1 < datetime.today():
            #         errors = "A data-alvo selecionada deve ser para depois do dia atual."
            #         return render(request, 'requestmanager/edit_outrosform.html',
            #                       {'formpedido': formpedido, 'errors': errors, 'min_date': min_date,
            #                        'max_date': max_date})

            old_pedidooutro.assunto_pedido = assunto_pedido
            old_pedidooutro.descricao_pedido = descricao_pedido
            old_pedidooutro.dataalvo_pedido = data_pedido
            old_pedidooutro.pedido_ptr_id = big_pedido
            objects.append(old_pedidooutro)

        for p in objects:
            p.save()
        big_pedido.save()

        '''Verificar pedidodinhos removidos'''
        # Pega nos pedidosoutros que estao ligado ao pedido principal
        # e verifica quais os que foram mandados no request
        # e elimina os que estão ligados ao pedido mas nao estao no request
        for pedido in pedidosoutro:
            if str(pedido.id) not in ids_atualizados:
                pedido.delete()

        messages.info(request, 'Pedido editado com sucesso')
        return redirect('/requestmanager/app/' + str(request.user.id))

    form = PedidoForm(
        initial={'assunto': big_pedido.assunto, 'descricao': big_pedido.descricao, 'data': big_pedido.dataalvo}
    )

    context = {
        "formpedido": form,
        "assunto_pedido": big_pedido.assunto,
        "desc_pedido": big_pedido.descricao,
        "error": error_data,
        'min_date': min_date,
        'max_date': max_date
    }
    return render(request, 'requestmanager/edit_outrosform.html', context)


################################
############ List ##############
################################

class app_render(SingleTableMixin, django_filters.views.FilterView):
    model = Pedido
    table_class = PedidoTable
    filterset_class = PedidoFilter
    template_name = 'requestmanager/app.html'

    def get_queryset(self):
        return Pedido.objects.all().filter(docente=self.kwargs['user_id'])

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/requestmanager/welcome/')
        elif request.user.groups.filter(name='Funcionario').exists():
            return redirect('/funcionariomanager/app/' + str(request.user.id))

        return super().dispatch(request, *args, **kwargs)


class app_renderUC(SingleTableMixin, django_filters.views.FilterView):
    model = Pedido
    table_class = PedidoTableUC
    filterset_class = PedidoFilterTipo
    template_name = 'requestmanager/list_unidadecurricular.html'

    def get_queryset(self):
        return Pedido.objects.all().filter(docente=self.kwargs['user_id'], tipo=3)


class app_renderOutros(SingleTableMixin, django_filters.views.FilterView):
    model = Pedido
    table_class = PedidoTableOutros
    filterset_class = PedidoFilterTipo
    template_name = 'requestmanager/list_outros.html'

    def get_queryset(self):
        return Pedido.objects.all().filter(docente=self.kwargs['user_id'], tipo=1)


class app_renderSalas(SingleTableMixin, django_filters.views.FilterView):
    model = Pedido
    table_class = PedidoTableSalas
    filterset_class = PedidoFilterTipo
    template_name = 'requestmanager/list_salas.html'

    def get_queryset(self):
        return Pedido.objects.all().filter(docente=self.kwargs['user_id'], tipo=2)


class app_renderHorario(SingleTableMixin, django_filters.views.FilterView):
    model = Pedido
    table_class = PedidoTableHorario
    filterset_class = PedidoFilterTipo
    template_name = 'requestmanager/list_horario.html'

    def get_queryset(self):
        return Pedido.objects.all().filter(docente=self.kwargs['user_id'], tipo=4)


def consult_pedido(request, pdd_id):
    if not request.user.is_authenticated:
        return redirect('/requestmanager/welcome/')

    pedido = Pedido.objects.get(pk=pdd_id)
    print(pedido.tipo_id)
    if pedido.tipo_id == 1:
        all_pedidos = list(Pedidooutros.objects.filter(pedido_ptr_id=pedido))
    elif pedido.tipo_id == 2:
        all_pedidos = list(Pedidosala.objects.filter(pedido_ptr_id=pedido))
    elif pedido.tipo_id == 3:
        all_pedidos = list(Pedidouc.objects.filter(pedido_ptr_id=pedido))
    else:
        all_pedidos = list(Pedidohorario.objects.filter(pedido_ptr_id=pedido))

    context = {
        "id": pdd_id,
        "Assunto": pedido.assunto,
        "Descrição": pedido.descricao,
        "Data_alvo": pedido.dataalvo,
        'all_pedidos': all_pedidos,
        'pendente': pedido.anoletivo == selectanoletivo() and pedido.estado_id == 1,
        'resolvido': pedido.anoletivo == selectanoletivo() and pedido.estado_id != 3 and pedido.estado_id == 2,
    }
    return render(request, 'requestmanager/consult_pedido.html', context)


def delete_pedido(request, pdd_id):
    if not request.user.is_authenticated:
        return redirect('/requestmanager/welcome/')

    if request.method == 'POST':
        pedido = Pedido.objects.get(pk=pdd_id)
        pedido.delete()
        messages.error(request, 'Pedido removido com sucesso')
        return redirect('/requestmanager/app/' + str(request.user.id))
    context = {
        "id": pdd_id
    }
    return render(request, 'requestmanager/delete_pedido.html', context)


# MENSAGEM SUCESSO

def sucesso_view(request, mensagem):
    if not request.user.is_authenticated:
        return redirect('/requestmanager/welcome/')

    return render(request, 'requestmanager/sucesso.html', {'message': mensagem, 'user_id': request.user.id})


def welcome_page_view(request):
    docentes = Group.objects.filter(name="docentes")
    funcionarios = Group.objects.filter(name="funcionarios")

    if request.user.is_authenticated:
        if request.user.groups.filter(name='ProfessorUniversitario').exists():
            return redirect('/requestmanager/app/' + str(request.user.id))
        elif request.user.groups.filter(name='Funcionario').exists():
            return redirect('/funcionariomanager/app/' + str(request.user.id))
    return render(request, 'requestmanager/welcome_page_2.html')


def try_model(pk, model):
    try:
        user = model.objects.get(pk=pk)
    except model.DoesNotExist:
        user = None
    return user
