from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from requestmanager.models import *
from authmanager.models import *
from .serializers import *
from rest_framework import permissions


class PedidoAPIView(APIView):
    def get(self, request, *args, **kwargs):
        pedidos = Pedido.objects.all()
        serializer = PedidoSerializer(pedidos, many=True)
        print(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PedidoDetailAPIView(APIView):
    def get(self, request, id, *args, **kwargs):
        pedidos = Pedido.objects.get(pk=id)
        serializer = PedidoSerializer(pedidos)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PedidoOutroAPIView(APIView):
    def get(self, request, *args, **kwargs):
        pedidos = Pedidooutros.objects.all()
        serializer = PedidoOutroSerializer(pedidos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PedidoUCDetailAPIView(APIView):
    def get(self, request, id, *args, **kwargs):
        pedidos = Pedidouc.objects.filter(pedido_ptr_id=id)
        serializer = PedidoUCSerializer(pedidos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PedidoOutrosDetailAPIView(APIView):
    def get(self, request, id, *args, **kwargs):
        pedidos = Pedidooutros.objects.filter(pedido_ptr_id=id)
        serializer = PedidoOutroSerializer(pedidos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PedidoUCDetailAPIView(APIView):
    def get(self, request, id, *args, **kwargs):
        pedidos = Pedidouc.objects.filter(pedido_ptr_id=id)
        serializer = PedidoUCSerializer(pedidos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PedidoSalaDetailAPIView(APIView):
    def get(self, request, id, *args, **kwargs):
        pedidos = Pedidosala.objects.filter(pedido_ptr_id=id)
        serializer = PedidoSalaSerializer(pedidos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class AcaoAPIView(APIView):
    def get(self, request, *args, **kwargs):
        acao = Acao.objects.all()
        serializer = AcaoSerializer(acao, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UnidadeCurricularAPIView(APIView):
    def get(self, request, id, *args, **kwargs):
        pedidos = Unidadecurricular.objects.filter(tipo=id)
        serializer = UnidadeCurricularesSerializer(pedidos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoriaSalaAPIView(APIView):
    def get(self, request, *args, **kwargs):
        categoria = Categoriasala.objects.all()
        serializer = CategoriaSalaSerializer(categoria, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PedidoHorarioDetailAPIView(APIView):
    def get(self, request, id, *args, **kwargs):
        pedidos = Pedidohorario.objects.filter(pedido_ptr_id=id)
        serializer = PedidohorarioSerializer(pedidos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FuncionarioAPIView(APIView):
    def get(self, *args, **kwargs):
        funcionarios = Funcionario.objects.all()
        serializer = FuncionarioSerializer(funcionarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class TipoPedidoSalaAPIView(APIView):
    def get(self, *args, **kwargs):
        tipos = Tipopedidosala.objects.all()
        serializer = TipoPedidoSalaSerializer(tipos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TipoTurmaAPIView(APIView):
    def get(self, *args, **kwargs):
        turma = TipoTurma.objects.all()
        serializer = TipoTurmaSerializer(turma, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)