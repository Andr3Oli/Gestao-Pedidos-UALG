from datetime import date
from .models import *
from django import forms
from django.forms import ModelForm, inlineformset_factory, BaseInlineFormSet, formset_factory


class DateInput(forms.DateInput):
    input_type = 'date'


class pedidoForm(forms.Form):
    assunto = forms.CharField(label='assunto', max_length=255, widget=forms.TextInput(attrs={"class":"block input"}))
    data = forms.DateField(label='date', widget=DateInput)
    descricao = forms.CharField(label='descricao', widget=forms.Textarea(attrs={"class":"block textarea"}))

class deletePedidoForm(forms.Form):
    confirmar = forms.CharField()


class criar_pedidoHorario(forms.Form):
    all_entries_tiposAH = Tipoalteracaohorario.objects.values_list('id', 'nome')
    all_entries = list(all_entries_tiposAH)

    uc_entries = Unidadecurricular.objects.values_list('id', 'nome').filter(tipo=3)
    all_uc_entries = list(uc_entries)

    enum_horario = Tipopedidohorario.objects.values_list('id', 'nome')
    enum_horario_choices = list(enum_horario)

    #########
    # assunto = forms.CharField(label="Assunto", max_length=100)
    #########

    # assunto = forms.CharField()
    # descricao = forms.CharField(label="Descrição", max_length=2000, widget=forms.Textarea)
    # data = forms.DateField(widget=DateInput)
    unidadeCurricular = forms.ChoiceField(label="Unidade Curricular", choices=all_uc_entries)
    tipoHorarioID = forms.ChoiceField(label="Tipo de horario", choices=enum_horario_choices)
    tipoAlteracaoID = forms.ChoiceField(label="Tipo de alteração", choices=all_entries)


formset_horario = formset_factory(criar_pedidoHorario, extra=2)


class editar_pedidoHorario(forms.Form):
    assunto = forms.CharField(label="assunto")
    data = forms.DateField(label="data", widget=DateInput)
    descricao = forms.CharField(label="descricao", max_length=2000, widget=forms.Textarea)


class apagar_pedidoHorario(forms.Form):
    id_pdd = forms.IntegerField(label="Id")


SEMESTRES = (
    ("1", "1º Semestre"),
    ("2", "2º Semestre"),
)

all_entries_tiposAcao = Acao.objects.values_list('id', 'nome')
all_acao = list(all_entries_tiposAcao)

all_entries_tiposUC = Unidadecurricular.objects.values_list('id', 'nome').filter(tipo="3")
all_unidadescurriculares = list(all_entries_tiposUC)

all_entries_tiposTurma = TipoTurma.objects.values_list('id', 'nome')
all_Turmas = list(all_entries_tiposTurma)

all_entries_tiposCS = Categoriasala.objects.values_list('id', 'nome')
all_CS = list(all_entries_tiposCS)

all_entries_salas = Sala.objects.values_list('id', 'sala')
all_salas = list(all_entries_salas)

CATEGORIA_SALA_CHOICES = (
    ("1", "Normal"),
    ("2", "Informática"),
)


class create_unidadesCurriculares(forms.Form):
    acao = forms.ChoiceField(choices=all_acao)
    unidadecurricular = forms.ChoiceField(choices=all_unidadescurriculares)
    turmas = forms.ChoiceField(choices=all_Turmas)
    assunto = forms.CharField()


UCFormSet = formset_factory(create_unidadesCurriculares, extra=2)


class edit_unidadesCurriculares(forms.Form):
    assunto = forms.CharField(label='assunto', max_length=255, widget=forms.TextInput(attrs={"class":"block input"}))
    data = forms.DateField(label='date', widget=DateInput)
    descricao = forms.CharField(label='descricao', widget=forms.Textarea(attrs={"class":"block textarea"}))


class delete_unidadesCurriculares(forms.Form):
    id = forms.CharField(max_length=30)


class pedidoSalaForm(forms.Form):
    acao = forms.ChoiceField(choices=all_acao)
    data = forms.DateField(widget=DateInput)
    lugares = forms.IntegerField(min_value=0, max_value=500, initial=0)
    hora_inicio = forms.TimeField()
    hora_fim = forms.TimeField()
    categoria_sala = forms.ChoiceField(choices=all_CS)
    unidade_curricular = forms.ChoiceField(choices=all_unidadescurriculares)


formset_sala = formset_factory(pedidoSalaForm, extra=2)

salaFormSet = formset_factory(pedidoSalaForm, extra=2)


class pedidoSalaDeleteForm(forms.Form):
    id = forms.IntegerField(min_value=0, initial=0)


class pedidoSalaEditForm(forms.Form):
    data = forms.DateField(label="data", widget=DateInput)
    assunto = forms.CharField(label="assunto")
    descricao = forms.CharField(label="descricao", widget=forms.Textarea)


class PedidoForm(forms.Form):
    assunto = forms.CharField(label='assunto', max_length=255, widget=forms.TextInput(attrs={"class": "block input"}))
    date = forms.DateField(label='date', widget=DateInput)
    descricao = forms.CharField(label='descricao', widget=forms.Textarea(attrs={"class":"block textarea"}))


class OutrosForm(forms.Form):
    assunto = forms.CharField(label='assunto', max_length=255)
    data = forms.DateField(widget=DateInput)
    descricao = forms.CharField(widget=forms.Textarea)


OutrosFormSet = formset_factory(OutrosForm, extra=2)


# OutrosFormSet = inlineformset_factory(Pedido, Pedidooutros, form=OutrosForm, fields=["assunto", "descricao", "data"],can_delete=True, extra=1)

class DeleteOutrosForm(forms.Form):
    id = forms.IntegerField()


class EditOutrosForm(forms.Form):
    descricao = forms.CharField(widget=forms.Textarea, label="descricao")
    assunto = forms.CharField(label='assunto', max_length=255)
    data = forms.DateField(widget=DateInput, label="data")
