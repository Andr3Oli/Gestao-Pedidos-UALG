from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from requestmanager.models import *
from authmanager.forms import *

docente_group, created_d = Group.objects.get_or_create(name='ProfessorUniversitario')
funcionario_group, created_f = Group.objects.get_or_create(name='Funcionario')


# def login_view(request):
#     if request.method == 'POST':
#         login_form = LoginForm(request.POST)
#         if login_form.is_valid():
#             email = request.POST["email"]
#             password = request.POST["password"]
#             try:
#                 temp_user = User.objects.get(email=email)
#                 user = authenticate(username=temp_user.username, password=password)
#             except User.DoesNotExist:
#                 user = None
#             if user is not None:
#                 login(request, user)
#                 meta_user = try_model(user.id, Conta)
#                 if meta_user is not None:
#                     return redirect('/requestmanager/app/' + str(user.id))
#                 else:
#                     return redirect('/funcionariomanager/app/' + str(user.id))
#             else:
#                 login_form = LoginForm()
#                 return render(request, 'login.html', context={'form': login_form})
#     else:
#         login_form = LoginForm()
#         return render(request, 'login.html', context={'form': login_form})
#

# def redirect_view(request):
#     print("tou aqui")
#     user = Conta.objects.get(pk=request.user.id)
#     print(user)
#
#
#
# def register(request):
#     if request.method == 'POST':
#         form = register_form(request.POST)
#         if form.is_valid():
#             ni = form.cleaned_data.get('ni')
#             email = form.cleaned_data.get('email')
#             password = form.cleaned_data.get('password')
#
#             meta_user = try_model(ni, Conta)
#             if meta_user == None:
#                 isDocente = False
#                 meta_user = try_model(ni, Funcionario)
#             else:
#                 isDocente = True
#             names = get_names(meta_user.nome)
#
#             user = User.objects.create_user(id=meta_user.id, username=meta_user.nome, email=email, password=password,
#                                             first_name=names[0], last_name=names[1])
#
#             if isDocente:
#                 user.groups.add(docente_group)
#             else:
#                 user.groups.add(funcionario_group)
#             user.save()
#
#             # user = authenticate(request, email=request.POST['email'], password=request.POST['password'])
#             if user is not None:
#                 login(request, user)
#                 # redirect_view(request)
#                 if isDocente:
#                     return redirect('/requestmanager/app/' + str(user.id))
#                 else:
#                     return redirect('/funcionariomanager/app/' + str(user.id))
#             else:
#                 print("print")
#         else:
#             print("invalid")
#
#     form = register_form()
#     context = {
#         'form': form,
#     }
#     return render(request, 'authmanager/register_user.html', context)


def criar_utilizador(request, id):
    if request.user.is_authenticated:
        return redirect('/requestmanager/welcome/')
    ''' Criar um novo utilizador que poderá ter de ser validado dependendo do seu tipo '''
    # if request.user.is_authenticated:
    #     user = get_user(request)
    #     if user.groups.filter(name="ProfessorUniversitario").exists():
    #         u = "ProfessorUniversitario"
    #     elif user.groups.filter(name="Funcionario").exists():
    #         u = "Funcionario"
    #     else:
    #         u = ""
    # else:
    u = ""
    msg = False
    if request.method == "POST":
        tipo = id
        if tipo == 1:
            form = ProfessorUniversitarioRegisterForm(request.POST)
            perfil = "Professor Universitario"
            my_group = Group.objects.get(name='ProfessorUniversitario')
        elif tipo == 2:
            form = FuncionarioRegisterForm(request.POST)
            perfil = "Funcionario"
            my_group = Group.objects.get(name='Funcionario')
        else:
            return redirect("utilizadores:escolher-perfil")

        print(form.is_valid())
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            my_group.user_set.add(user)

            if tipo == 1:
                user.valido = 'True'
                user.save()
                p = 1
            elif tipo == 2:
                user.valido = 'True'
                recipient_id = user.id  # Enviar Notificacao Automatica !!!!!!!!!
                user.save()
                p = 2
                # views.enviar_notificacao_automatica(request, "validarRegistosPendentes",
                #                                     recipient_id)  # Enviar Notificacao Automatica !!!!!!!!!

            return redirect("authmanager:concluir_registo", p)
        else:
            print("INVALIDO")
            msg = True
            tipo = id
            return render(request=request,
                          template_name="authmanager/register_user.html",
                          context={"form": form, 'perfil': perfil, 'u': u, 'registo': tipo, 'msg': msg})
    else:
        tipo = id
        if tipo == 2:
            form = FuncionarioRegisterForm()
            perfil = "Funcionario"
        elif tipo == 1:
            form = ProfessorUniversitarioRegisterForm()
            perfil = "Professor Universitario"
        else:
            return redirect("authmanager:escolher-perfil")
    return render(request=request,
                  template_name="authmanager/register_user.html",
                  context={"form": form, 'perfil': perfil, 'u': u, 'registo': tipo, 'msg': msg})


def logout_view(request):
    logout(request)
    return redirect('/requestmanager/welcome/')


def get_names(nome):
    index1 = str(nome).find(' ')
    index2 = str(nome).rfind(' ')
    first_name = str(nome)[0:index1]
    last_name = str(nome)[index2:len(nome)]
    return [first_name, last_name]


def try_model(pk, model):
    try:
        user = model.objects.get(pk=pk)
    except model.DoesNotExist:
        user = None
    return user


def escolher_perfil(request):
    utilizadores = ["Professor Universitário", "Funcionário"]
    context = {
        'utilizadores': utilizadores
    }
    return render(request, 'escolher_pefil.html', context)


def concluir_registo(request, id):
    ''' Página que é mostrada ao utilizador quando faz um registo na plataforma '''

    return render(request=request,
                  template_name="concluir_registo.html")


def load_departamentos(request):
    ''' Carregar todos os departamentos para uma determinada faculdade '''
    faculdadeid = request.GET.get('faculdade')
    departamentos = Departamento.objects.filter(faculdadeid=faculdadeid).order_by('nome')
    print(departamentos)
    return render(request, 'departamento_dropdown_list_options.html', {'departamentos': departamentos})


def login_action(request):
    ''' Fazer login na plataforma do dia aberto e gestão de acessos à plataforma '''
    if request.user.is_authenticated:
        return redirect('/requestmanager/welcome/')

    u = ""
    msg = False
    error = ""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == "" or password == "":
            msg = True
            error = "Todos os campos são obrigatórios!"
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                utilizador = Utilizador.objects.get(id=user.id)
                if utilizador.valido == "False":
                    msg = True
                    error = "O seu registo ainda não foi validado"
                elif utilizador.valido == "Rejeitado":
                    msg = True
                    error = "O seu registo não é válido"
                else:
                    login(request, user)
                    return redirect('authmanager:mensagem', 1)
            else:
                msg = True
                error = "O nome de utilizador ou a palavra-passe inválidos!"
    form = LoginForm()
    return render(request=request,
                  template_name="login.html",
                  context={"form": form, "msg": msg, "error": error, 'u': u})


def mensagem(request, id, *args, **kwargs):
    ''' Template de mensagens informativas/erro/sucesso '''

    if request.user.is_authenticated:
        user = request.user
        if user.groups.filter(name="Coordenador").exists():
            u = "Coordenador"
        elif user.groups.filter(name="Administrador").exists():
            u = "Administrador"
        elif user.groups.filter(name="ProfessorUniversitario").exists():
            u = "ProfessorUniversitario"
        elif user.groups.filter(name="Colaborador").exists():
            u = "Colaborador"
        elif user.groups.filter(name="Participante").exists():
            u = "Participante"
        else:
            u = ""
    else:
        u = ""

    if id == 400 or id == 500:
        user = request.user
        m = "Erro no servidor"
        tipo = "error"
    elif id == 1:
        user = request.user
        m = "Bem vindo(a) " + user.first_name
        tipo = "info"

    elif id == 2:
        m = "Até á próxima!"
        tipo = "info"

    elif id == 3:
        m = "Registo feito com sucesso!"
        tipo = "sucess"

    elif id == 4:
        m = "É necessário fazer login primeiro"
        tipo = "error"

    elif id == 5:
        m = "Não permitido"
        tipo = "error"
    elif id == 6:
        m = "Senha alterada com sucesso!"
        tipo = "success"
    elif id == 7:
        m = "Conta apagada com sucesso"
        tipo = "success"
    elif id == 8:
        m = "Perfil alterado com sucesso"
        tipo = "success"
    elif id == 9:
        m = "Perfil criado com sucesso"
        tipo = "success"
    elif id == 10:
        m = "Não existem notificações"
        tipo = "info"
    elif id == 11:
        m = "Esta tarefa deixou de estar atribuída"
        tipo = "error"
    elif id == 12:
        m = "Ainda não é permitido criar inscrições"
        tipo = "error"
    elif id == 13:
        m = "Erro ao apagar dados do utilizador"
        tipo = "error"
    elif id == 14:
        m = "Não existem mensagens"
        tipo = "info"
    elif id == 15:
        m = "Este colaborador tem tarefas iniciadas pelo que apenas deverá ser apagado quando estas estiverem concluidas"
        tipo = "info"
    elif id == 16:
        m = "Para puder apagar a sua conta deverá concluir primeiro as tarefas que estão iniciadas"
        tipo = "info"
    elif id == 17:
        m = "A sua disponibilidade foi alterada com sucesso"
        tipo = "success"
    elif id == 18:
        m = "Antes de poder ver dados e estatísticas é preciso configurar um Dia Aberto."
        tipo = "error"
    else:
        m = "Esta pagina não existe"
        tipo = "error"

    continuar = "on"
    if id == 400 or id == 500:
        continuar = "off"
    return render(request=request,
                  template_name="mensagem.html", context={'m': m, 'tipo': tipo, 'u': u, 'continuar': continuar, })
