from rest_framework import serializers
from requestmanager.models import *


class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = ['assunto', 'descricao', 'dataalvo', 'estado']


class PedidoOutroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedidooutros
        fields = ['id', 'assunto_pedido', 'descricao_pedido', 'dataalvo_pedido', 'pedido_ptr_id']


class PedidoUCSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedidouc
        fields = ['id', 'acao', 'unidadecurricularid', 'tipoturmaid', 'assunto', 'pedido_ptr_id']


class PedidoSalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedidosala
        fields = ['id', 'pedido_ptr_id', 'acao', 'data', 'alunosprevistos', 'horainicio', 'horafim', 'tipopedidosalaid',
                  'categoriasalaid']


class PedidohorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedidohorario
        fields = ['id', 'acao', 'tipoalteracaohorarioid', 'dataorigem', 'horaorigem', 'datamudanca',
                  'horamudanca', 'descricao']


class UnidadeCurricularesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unidadecurricular
        fields = ['id', 'nome']


class AcaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acao
        fields = ['id', 'nome']


class CategoriaSalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoriasala
        fields = ['id', 'nome']


class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = ['id', 'username']

class TipoPedidoSalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipopedidosala
        fields = ['id', 'nome']
        
class TipoTurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoTurma
        fields = ['id', 'nome']
