from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import *
from rest_framework import viewsets, permissions, status
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

#ViewSets
class VendedorViewSet(viewsets.ModelViewSet):
    queryset = Vendedor.objects.all()
    serializer_class = VendedorSerializer
    permission_classes = [(permissions.IsAdminUser & permissions.IsAuthenticated) | permissions.IsAuthenticatedOrReadOnly]

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    permission_classes = [(permissions.IsAdminUser & permissions.IsAuthenticated)]
    serializer_class = ClienteSerializer

class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    permission_classes = [(permissions.IsAdminUser & permissions.IsAuthenticated) | permissions.IsAuthenticatedOrReadOnly]
    serializer_class = MarcaSerializer

class TipoArticuloViewSet(viewsets.ModelViewSet):
    queryset = TipoArticulo.objects.all()
    permission_classes = [(permissions.IsAdminUser & permissions.IsAuthenticated) | permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TipoArticuloSerializer

class ArticuloViewSet(viewsets.ModelViewSet):
    queryset = Articulo.objects.all()
    permission_classes = [(permissions.IsAdminUser & permissions.IsAuthenticated) | permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ArticuloSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [(permissions.IsAdminUser & permissions.IsAuthenticated) | permissions.IsAuthenticated]

class CarritoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = CarritoSerializer
    permission_classes = [permissions.IsAuthenticated]

#Pedido 
class PedidoView(APIView):
    def post(self, request):
        serializer = PedidoSerializer()
        pedido = serializer.create_pedido(request.data)

        return Response(PedidoSerializer(pedido).data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        pedido = Pedido.objects.get(pk=pk)
        pedido.eliminar()
        return Response(status=status.HTTP_204_NO_CONTENT)