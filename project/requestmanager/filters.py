import django_tables2 as tables
from .models import *
from django.utils.html import format_html
import django_filters
from django import forms

class PedidoFilter(django_filters.FilterSet):
    class Meta:
        model = Pedido
        fields = ['estado', 'tipo']
    assunto = django_filters.CharFilter(field_name='assunto', lookup_expr='icontains')
    DataAlvo = django_filters.DateFilter(field_name='dataalvo')
    DataAlvo__lt = django_filters.DateFilter(field_name='dataalvo', lookup_expr='lt')
    DataAlvo__gt = django_filters.DateFilter(field_name='dataalvo', lookup_expr='gt' )
    
class PedidoFilterTipo(django_filters.FilterSet):
    class Meta:
        model = Pedido
        fields = ['estado']
    assunto = django_filters.CharFilter(field_name='assunto', lookup_expr='icontains')
    DataAlvo = django_filters.DateFilter(field_name='dataalvo')
    DataAlvo__lt = django_filters.DateFilter(field_name='dataalvo', lookup_expr='lt')
    DataAlvo__gt = django_filters.DateFilter(field_name='dataalvo', lookup_expr='gt' )
    
    