import django_tables2 as tables
from .models import *
from django.utils.html import format_html
import django_filters
from django import forms
from requestmanager.models import *
from authmanager.models import *

class NumberInFilter(django_filters.CharFilter, django_filters.NumberFilter):
    pass

class PedidoFilter(django_filters.FilterSet):
    class Meta:
        model = Pedido
        fields = ['estado', 'tipo', 'anoletivo']
    DataAlvo = django_filters.DateFilter(field_name='dataalvo')
    DataAlvo__lt = django_filters.DateFilter(field_name='dataalvo', lookup_expr='lt')
    DataAlvo__gt = django_filters.DateFilter(field_name='dataalvo', lookup_expr='gt' )
    docente__username = django_filters.CharFilter(lookup_expr='icontains')
    responsavel__username = django_filters.CharFilter(lookup_expr='icontains')
    