from django import forms
from requestmanager.models import *

class DateInput(forms.DateInput):
    input_type = 'date'

all_entries_anoletivo = AnoLetivo.objects.values_list('id', 'nome')
all_anoletivo = list(all_entries_anoletivo)

class UploadFileForm(forms.Form):
    file = forms.FileField()
    anoletivo = forms.ChoiceField(choices=all_anoletivo)

class UploadFileFormRUC(forms.Form):
    file = forms.FileField()

all_entries_tiposAH = (
    ("1", "Todos"),
    ("2", "Salas"),
    ("3", "Unidades Curriculares"),
    ("4", "Horários"),
    ("5", "Outros"),
    ("6", "Selecionados"),
)
all_entries = list(all_entries_tiposAH)
    
class ExportFileForm(forms.Form):
    tipodePedido = forms.ChoiceField(label="tipodepedido", choices=all_entries)
    
    
    