from .models import *
from requestmanager.models import *
from django import forms
from django.forms import CharField, PasswordInput, TextInput, ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from authmanager.models import Faculdade, Funcionario, ProfessorUniversitario, Departamento



class LoginForm(AuthenticationForm):
    username=CharField(widget=TextInput(attrs={'class':'input','style':''}), label="Nome de Utilizador", max_length=255, required=False)
    password=CharField(widget=PasswordInput(attrs={'class':'input','style':''}), label= 'Senha', max_length=255, required=False)


class register_form(forms.Form):
    ni = forms.IntegerField(label="Numero de indentificação", required=True)
    email = forms.EmailField(label="Email", required=True)
    password = forms.CharField(label="Password", required=True, widget=forms.PasswordInput)


# class AdministradorRegisterForm(UserCreationForm):
#     class Meta:
#         model = Administrador
#         fields = ('username', 'password1', 'password2', 'email',
#                   'first_name', 'last_name', 'contacto', 'gabinete')
#
#     def clean(self):
#         username = self.cleaned_data.get('username')
#         password1 = self.cleaned_data.get('password1')
#         password2 = self.cleaned_data.get('password2')
#         email = self.cleaned_data.get('email')
#         first_name = self.cleaned_data.get('first_name')
#         last_name = self.cleaned_data.get('last_name')
#         contacto = self.cleaned_data.get('contacto')
#         gabinete = self.cleaned_data.get('gabinete')
#         erros = []
#         if email == "" or first_name == "" or last_name == "" or username == None or gabinete == None:
#             raise forms.ValidationError(f'Todos os campos são obrigatórios!')
#
#         if username and User.objects.filter(username=username).exists():
#             erros.append(forms.ValidationError(f'O username já existe'))
#
#         if password1 == None or password2 == None:
#             if password1 == None:
#                 raise forms.ValidationError(f'Todos os campos são obrigatórios!')
#             if password1 == None:
#                 raise forms.ValidationError(f'Todos os campos são obrigatórios!')
#             else:
#                 erros.append(forms.ValidationError(f'As palavras-passe não correspondem'))
#
#         if email and User.objects.filter(email=email).exclude(username=username).exists():
#             raise forms.ValidationError(f'O email já existe')
#         elif email == None:
#             erros.append(forms.ValidationError(f'O email é inválido'))
#
#         if contacto == None:
#             erros.append(forms.ValidationError(f'Preencha corretamente o contacto'))
#         if len(erros) > 0:
#             raise ValidationError([erros])


class ProfessorUniversitarioRegisterForm(UserCreationForm):
    class Meta:
        model = ProfessorUniversitario
        fields = ('username', 'password1', 'password2', 'email',
                  'first_name', 'last_name', 'contacto', 'gabinete', 'faculdade', 'departamento')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['departamento'].queryset = Departamento.objects.none()

        if 'faculdade' in self.data:
            try:
                faculdadeid = int(self.data.get('faculdade'))
                self.fields['departamento'].queryset = Departamento.objects.filter(
                    faculdadeid=faculdadeid).order_by('nome')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['departamento'].queryset = self.instance.faculdade.departamento_set.order_by('nome')

    def clean(self):
        username = self.cleaned_data.get('username')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        email = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        contacto = self.cleaned_data.get('contacto')
        gabinete = self.cleaned_data.get('gabinete')
        faculdade = self.cleaned_data.get('faculdade')
        departamento = self.cleaned_data.get('departamento')
        erros = []
        if email == "" or first_name == "" or last_name == "" or username is None or gabinete is None or faculdade is None or departamento is None:
            raise forms.ValidationError(f'Todos os campos são obrigatórios!')

        if username and User.objects.filter(username=username).exists():
            erros.append(forms.ValidationError(f'O username já existe'))

        if password1 is None or password2 is None:
            if password1 is None:
                raise forms.ValidationError(f'Todos os campos são obrigatórios!')
            if password1 is None:
                raise forms.ValidationError(f'Todos os campos são obrigatórios!')
            else:
                erros.append(forms.ValidationError(f'As palavras-passe não correspondem'))

        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(f'O email já existe')
        elif email is None:
            erros.append(forms.ValidationError(f'O email é inválido'))

        if contacto is None:
           erros.append(forms.ValidationError(f'Preencha corretamente o contacto'))
        print(contacto)
        print(erros)
        if len(erros) > 0:
            raise ValidationError([erros])


class FuncionarioRegisterForm(UserCreationForm):
    class Meta:
        model = Funcionario
        fields = ('username', 'password1', 'password2', 'email',
                  'first_name', 'last_name', 'contacto', 'gabinete', 'faculdade')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        email = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        contacto = self.cleaned_data.get('contacto')
        gabinete = self.cleaned_data.get('gabinete')
        faculdade = self.cleaned_data.get('faculdade')
        erros = []
        if email == "" or first_name == "" or last_name == "" or username is None or gabinete is None or faculdade is None:
            raise forms.ValidationError(f'Todos os campos são obrigatórios!')

        if username and User.objects.filter(username=username).exists():
            erros.append(forms.ValidationError(f'O username já existe'))

        if password1 is None or password2 is None:
            if password1 is None:
                raise forms.ValidationError(f'Todos os campos são obrigatórios!')
            if password1 is None:
                raise forms.ValidationError(f'Todos os campos são obrigatórios!')
            else:
                erros.append(forms.ValidationError(f'As palavras-passe não correspondem'))

        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(f'O email já existe')
        elif email is None:
            erros.append(forms.ValidationError(f'O email é inválido'))

        if contacto is None:
            erros.append(forms.ValidationError(f'Preencha corretamente o contacto'))
        if len(erros) > 0:
            raise ValidationError([erros])
