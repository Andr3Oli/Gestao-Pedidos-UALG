import csv
from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist
from requestmanager.models import *
from django.core.exceptions import ObjectDoesNotExist
import xlwt
import xlrd
from django.http import HttpResponse, HttpResponseRedirect
import pandas as pd
from datamanager.forms import *

from authmanager.models import *

from django_tables2 import *
from .tables import *
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin


#################################################
##### Ordem:                                #####
#####      -Importar Docentes               #####
#####      -Importar DSD                    #####
#####      -Importar Salas                  #####
#####      -Importar RUC                    #####
#####      -Exportar Pedidos                #####
#####      -Mensagem Sucesso                #####
#################################################


#################################################################################
######### Importar Docentes           ###########################################
######### Autor: Gonçalo Almeida      ###########################################
#################################################################################

def importdocentesxls(request):
    if not request.user.is_authenticated or request.user.groups.filter(name="ProfessorUniversitario").exists():
        return redirect('/requestmanager/welcome/')

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        campos_necessarios = ['Código', 'Ativo', 'Docente']
        if form.is_valid():
            file_name = request.FILES['file']
            idanoletivo = request.POST['anoletivo']
            if file_name.name.endswith('.xls'):
                sheet = pd.read_excel(file_name)
                colunas = list(sheet.columns)
                if all(campo in colunas for campo in campos_necessarios):
                    for index in range(len(sheet)):
                        try:
                            docente = Conta.objects.get(pk=sheet['Código'][index])
                            docente.ativo = sheet['Ativo'][index]
                            docente.save()
                        except ObjectDoesNotExist:
                            docente = Conta.objects.create(id=sheet['Código'][index], nome=sheet['Docente'][index],
                                                           ativo=sheet['Ativo'][index], tipocontaid_id=1,
                                                           idanoletivo=AnoLetivo.objects.get(pk=idanoletivo))
                    return sucesso_view(request, 'Docentes foram importados com sucesso!')
                else:
                    return erro_view(request, 'Ficheiro não contém os campos necessários')
            else:
                return erro_view(request, 'Ficheiro não é do tipo .xls')
    else:
        form = UploadFileForm()
    return render(request, 'datamanager/importDocente.html', {'form': form})


#######################################################################################
######### Importar DSD (Distribuição Serviço Docentes)  ###############################
######### Autor: António Madureira                      ###############################
#######################################################################################

def import_DSD(request):
    if not request.user.is_authenticated or request.user.groups.filter(name="ProfessorUniversitario").exists():
        return redirect('/requestmanager/welcome/')

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        campos_necessarios = ['Turma', 'Cód. disciplina', 'Cód. Docente']
        if form.is_valid():
            input_excel = request.FILES['file']
            idanoletivo = request.POST['anoletivo']
            if input_excel.name.endswith('.xls'):
                dataframe = pd.read_excel(input_excel)
                colunas = list(dataframe.columns)
                if all(campo in colunas for campo in campos_necessarios):
                    lenght = len(dataframe['Turma'].tolist())
                    dsd_data_manage(dataframe['Cód. disciplina'].tolist(), dataframe['Cód. Docente'].tolist(),
                                    dataframe['Turma'].tolist(), lenght, idanoletivo)
                    return sucesso_view(request, 'DSD foi importado com sucesso!')
                else:
                    return erro_view(request, 'Ficheiro não contém os campos necessários')
            else:
                return erro_view(request, 'Ficheiro não é do tipo .xls')
    else:
        form = UploadFileForm()
    return render(request, 'datamanager/importDSD.html', {'form': form})


def dsd_data_manage(disciplina, docente, turma, lenght, idanoletivo):
    for i in range(lenght):
        try:
            x = Dsd.objects.filter(unidadecurricularid_id=disciplina[i], turma=turma[i])
            if x.count():
                continue

            dsd = Dsd()
            dsd.turma = turma[i]
            dsd.unidadecurricularid = Unidadecurricular.objects.get(pk=disciplina[i])
            dsd.contaid = Conta.objects.get(pk=docente[i])
            dsd.idanoletivo = AnoLetivo.objects.get(pk=idanoletivo)
            dsd.save()
        except ObjectDoesNotExist:
            continue
    return


######################################################################
######### Importar Salas               ###############################
######### Autor: Tomás Roma            ###############################
######################################################################

def import_salas(request):
    if not request.user.is_authenticated or request.user.groups.filter(name="ProfessorUniversitario").exists():
        return redirect('/requestmanager/welcome/')

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        campos_necessarios = ['Desc. Edifício', 'Desc. Sala', 'Des. Categoria']
        if form.is_valid():
            input_excel = request.FILES['file']
            idanoletivo = request.POST['anoletivo']
            if input_excel.name.endswith('.xlsx'):
                dataframe = pd.read_excel(input_excel)
                colunas = list(dataframe.columns)
                if all(campo in colunas for campo in campos_necessarios):
                    lenght = len(dataframe['Desc. Edifício'])
                    salasFile_split(lenght, dataframe['Desc. Edifício'], dataframe['Desc. Sala'],
                                    dataframe['Des. Categoria'], dataframe['Lotação presencial sala'], idanoletivo)
                    return sucesso_view(request, 'Salas foram importadas com sucesso!')
                else:
                    return erro_view(request, 'Ficheiro não contém os campos necessários')
            else:
                return erro_view(request, 'Ficheiro não é do tipo .xlsx')
    else:
        form = UploadFileForm()
    return render(request, 'datamanager/importSalas.html', {'form': form})


def salasFile_split(lenght, Edi, sala, cat, lot, anoletivo):
    for i in range(lenght):
        # print( "ESTE É O CAT:", cat[i])
        new_sala = Sala()
        new_sala.edificio = str(Edi[i])
        new_sala.sala = str(sala[i])
        new_sala.lotacao = int(lot[i])
        new_sala.idanoletivo = AnoLetivo.objects.get(pk=anoletivo)
        if str(cat[i]) == "nan":
            new_sala.categoriasalaid = None
        else:
            new_sala.categoriasalaid = parse_catSala(cat[i])
        # print(new_sala)
        new_sala.save()
    return


def parse_catSala(cat):
    start = str(cat).rfind('[')
    end = str(cat).rfind(']')
    catpk = str(cat)[start + 1:end]
    catnome = str(cat)[0:start - 1]
    # print(catnome)
    # print(catpk)
    catS = Categoriasala.objects.get_or_create(pk=catpk, nome=catnome)
    return catS[0]


######################################################################
######### Exportar Pedidos / Importar RUC  ###########################
######### Autor: André Oliveira            ###########################
######################################################################

def export_pedidos_xls(request):
    if not request.user.is_authenticated or request.user.groups.filter(name="ProfessorUniversitario").exists():
        return redirect('/requestmanager/welcome/')

    if request.method == 'POST':
        selected_ids = request.POST.getlist('id')
        tipodePedido = request.POST.get('tipodePedido')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="pedidos.csv"'

        if tipodePedido == "3":
            users = Pedido.objects.all().filter(tipo='3')
        if tipodePedido == "5":
            users = Pedido.objects.all().filter(tipo='1')
        if tipodePedido == "2":
            users = Pedido.objects.all().filter(tipo='2')
        if tipodePedido == "4":
            users = Pedido.objects.all().filter(tipo='4')
        if tipodePedido == "1":
            users = Pedido.objects.all()
        if tipodePedido == "6":
            users = Pedido.objects.filter(pk__in=selected_ids)

        PedidoGeral = []
        for i in users:
            linha = {'Responsavel': i.responsavel,
                     'Descricao': i.descricao,
                     'Ano Letivo': i.anoletivo.nome,
                     'Tipo': i.tipo,
                     'Estado': i.estado,
                     'Assunto': i.assunto,
                     }
            PedidoGeral.append(linha)

            if "Unidades" in str(i.tipo):
                users_UC = Pedidouc.objects.all().filter(pedido_ptr_id=i.id)
                for f in users_UC:
                    linhaUC = {'Acao': f.acao,
                               'Unidade Curricular': f.unidadecurricularid.nome,
                               'Tipo turma': f.tipoturmaid.nome,
                               'Assunto PedidoUC': f.assunto}
                    PedidoGeral.append(linhaUC)
                PedidoGeral.append({})
            if "Horários" in str(i.tipo):
                users_UC = Pedidohorario.objects.all().filter(pedido_ptr_id=i.id)
                for f in users_UC:
                    linhaUC = {'Descricao Pedido': f.descricao,
                               'Acao': f.acao,
                               'Tipo Alteracao Horario': f.tipoalteracaohorarioid.nome,
                               'Data Origem': f.dataorigem,
                               'Hora Origem': f.horaorigem,
                               'Data Mudanca': f.datamudanca,
                               'Hora Mudanca': f.horamudanca}
                    PedidoGeral.append(linhaUC)
                PedidoGeral.append({})
            if "Outros" in str(i.tipo):
                users_UC = Pedidooutros.objects.all().filter(pedido_ptr_id=i.id)
                for f in users_UC:
                    linhaUC = {'Assunto': f.assunto_pedido,
                               'Descricao Pedido': f.descricao_pedido,
                               'Data Alvo': f.dataalvo_pedido}
                    PedidoGeral.append(linhaUC)
                PedidoGeral.append({})
            if "Salas" in str(i.tipo):
                users_UC = Pedidosala.objects.all().filter(pedido_ptr_id=i.id)
                for f in users_UC:
                    linhaUC = {'Data': f.data,
                               'Alunos Previstos': f.alunosprevistos,
                               'Hora Inicio': f.horainicio,
                               'Hora Fim': f.horafim,
                               'Tipo Pedido Sala': f.tipopedidosalaid.nome,
                               'Categoria Sala': f.categoriasalaid.nome}
                    PedidoGeral.append(linhaUC)
                PedidoGeral.append({})

        df = pd.DataFrame(PedidoGeral)
        response.write(df.to_csv())
        return response

    else:
        form = ExportFileForm()
    tables = PedidoTable(Pedido.objects.all())
    return render(request, 'datamanager/export.html', {'form': form, "table": tables})


def import_RUC(request):
    if not request.user.is_authenticated or request.user.groups.filter(name="ProfessorUniversitario").exists():
        return redirect('/requestmanager/welcome/')

    if request.method == 'POST':
        form = UploadFileFormRUC(request.POST, request.FILES)
        campos_necessarios = ['Docente', 'Ano letivo', 'Regência', 'Tipo']
        if form.is_valid():
            input_excel = request.FILES['file']
            if input_excel.name.endswith('.xls'):
                dataframe1 = pd.read_excel(input_excel)
                colunas = list(dataframe1.columns)
                if all(campo in colunas for campo in campos_necessarios):
                    val = len(str(dataframe1['Ano letivo'].tolist()).split("',"))
                    func_Split(str(dataframe1['Docente'].tolist()), val, str(dataframe1['Ano letivo'].tolist()),
                               str(dataframe1['Regência'].tolist()), str(dataframe1['Tipo'].tolist()))
                    return sucesso_view(request, 'RUC foi importado com sucesso!')
                else:
                    return erro_view(request, 'Ficheiro não contém os campos necessários')
            else:
                return erro_view(request, 'Ficheiro não é do tipo .xls')
    else:
        form = UploadFileFormRUC()
    return render(request, 'datamanager/importRUC.html', {'form': form})


def func_Split(docentes, lenght, Anoletivo, regencia, tipo):
    if lenght > 1:
        i = 0
        while i < lenght - 1:
            if AnoLetivo.objects.values_list('id').filter(nome=str(Anoletivo.split("',")[i][2:])):
                ruc = RUC()
                uc = Unidadecurricular()
                conta = Conta()
                uc.id = (str(regencia.split("',")[i][2:]).split('(')[-1])[:-1]
                uc.nome = (str(regencia.split("',")[i][2:]).rpartition('(')[0])
                conta.id = str(docentes.split("',")[i][2:]).split(" - ")[0]
                conta.nome = str(docentes.split("',")[i][2:]).split(" - ")[1]
                conta.tipocontaid = Tipoconta.objects.get(pk=1)
                if "curso" in tipo.split("',")[i]:
                    uc.tipo = Tiporegencia.objects.get(pk=1)
                if "departamento" in tipo.split("',")[i]:
                    uc.tipo = Tiporegencia.objects.get(pk=2)
                if "disciplina" in tipo.split("',")[i]:
                    uc.tipo = Tiporegencia.objects.get(pk=3)
                uc.save()
                conta.save()
                ruc.iduc = Unidadecurricular.objects.get(pk=uc.id)
                ruc.idconta = Conta.objects.get(pk=conta.id)
                var = list(AnoLetivo.objects.values_list('id').filter(nome=str(Anoletivo.split("',")[i][2:])))
                ruc.idanoletivo = AnoLetivo.objects.get(pk=int(str(var[0])[1:-2]))
                ruc.save()
            i += 1
        if AnoLetivo.objects.values_list('id').filter(nome=str(Anoletivo.split("',")[lenght - 1][2:-2])):
            ruc = RUC()
            conta = Conta()
            uc = Unidadecurricular()
            uc.id = (str(regencia.split("',")[lenght - 1][2:-2]).split('(')[-1])[:-1]
            uc.nome = (str(regencia.split("',")[lenght - 1][2:]).rpartition('(')[0])
            conta.id = str(docentes.split("',")[lenght - 1][2:]).split(" - ")[0]
            conta.nome = str(docentes.split("',")[lenght - 1][2:-2]).split(" - ")[1]
            conta.tipocontaid = Tipoconta.objects.get(pk=1)
            if "curso" in tipo.split("',")[lenght - 1]:
                uc.tipo = Tiporegencia.objects.get(pk=1)
            if "departamento" in tipo.split("',")[lenght - 1]:
                uc.tipo = Tiporegencia.objects.get(pk=2)
            if "disciplina" in tipo.split("',")[lenght - 1]:
                uc.tipo = Tiporegencia.objects.get(pk=3)
            uc.save()
            conta.save()
            ruc.iduc = Unidadecurricular.objects.get(pk=uc.id)
            ruc.idconta = Conta.objects.get(pk=conta.id)
            var = list(AnoLetivo.objects.values_list('id').filter(nome=str(Anoletivo.split("',")[lenght - 1][2:-2])))
            ruc.idanoletivo = AnoLetivo.objects.get(pk=int(str(var[0])[1:-2]))
            ruc.save()
    else:
        if AnoLetivo.objects.values_list('id').filter(nome=str(Anoletivo.split("',")[0][2:-2])):
            uc = Unidadecurricular()
            conta = Conta()
            ruc = RUC()
            uc.id = (str(regencia.split("',")[0][2:-2]).split('(')[-1])[:-1]
            uc.nome = (str(regencia.split("',")[0][2:]).rpartition('(')[0])
            conta.id = str(docentes.split("',")[0][2:]).split(" - ")[0]
            conta.nome = str(docentes.split("',")[0][2:-2]).split(" - ")[1]
            conta.tipocontaid = Tipoconta.objects.get(pk=1)
            if "curso" in tipo.split("',")[0]:
                uc.tipo = Tiporegencia.objects.get(pk=1)
            if "departamento" in tipo.split("',")[0]:
                uc.tipo = Tiporegencia.objects.get(pk=2)
            if "disciplina" in tipo.split("',")[0]:
                uc.tipo = Tiporegencia.objects.get(pk=3)
            uc.save()
            conta.save()
            ruc.iduc = Unidadecurricular.objects.get(pk=uc.id)
            ruc.idconta = Conta.objects.get(pk=conta.id)
            var = list(AnoLetivo.objects.values_list('id').filter(nome=str(Anoletivo.split("',")[lenght - 1][2:-2])))
            ruc.idanoletivo = AnoLetivo.objects.get(pk=int(str(var[0])[1:-2]))
            ruc.save()
    return


# Mensagem Sucesso

def sucesso_view(request, mensagem):
    if not request.user.is_authenticated:
        return redirect('/requestmanager/welcome/')

    return render(request, 'datamanager/sucesso.html', {'message': mensagem})


def erro_view(request, mensagem):
    if not request.user.is_authenticated:
        return redirect('/requestmanager/welcome/')

    return render(request, 'datamanager/erro.html', {'message': mensagem})
