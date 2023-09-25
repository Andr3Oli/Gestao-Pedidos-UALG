from .models import *
from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class create_AnoLetivo(forms.Form):
    datainicio = forms.DateField(label="data", widget=DateInput)
    datafim = forms.DateField(label="data", widget=DateInput)

class edit_AnoLetivo(forms.Form):
    datainicio = forms.DateField(label="data", widget=DateInput)
    datafim = forms.DateField(label="data", widget=DateInput)
    
class email_PCP(forms.Form):
    assunto = forms.CharField(label='assunto', max_length=255, widget=forms.TextInput(attrs={"class":"block input"}))
    descricao = forms.CharField(label='descricao', widget=forms.Textarea(attrs={"class":"block textarea"}))
    
class messageForm(forms.Form):
    messagem = forms.CharField(label='messagem', max_length=255, widget=forms.TextInput(attrs={"class":"block textarea"}))