from datetime import date
from django import forms
from django.forms import DateInput, ModelForm, inlineformset_factory, BaseInlineFormSet, formset_factory
from requestmanager.models import *


class stat_form(forms.Form):
    
    TipoPedidoEntries = TipoPedido.objects.values_list('id', 'nome')
    TipoPedidoEntries = list(TipoPedidoEntries)
    todos = (5, 'Todos')
    TipoPedidoEntries.append(todos)
    
    print(TipoPedidoEntries)
    
    AnoLetivoEntries = AnoLetivo.objects.values_list('id', 'nome')
    AnoLetivoEntries = list(AnoLetivoEntries)
    
    ano_letivo = forms.ChoiceField(label="Ano Letivo", choices=AnoLetivoEntries)
    tipo = forms.ChoiceField(label="Tipo de pedido", choices=TipoPedidoEntries)
    
    
    