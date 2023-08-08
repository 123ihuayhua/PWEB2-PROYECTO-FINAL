from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import *

class VendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendedor
        fields = ('id', 'VenDNI', 'VenApePat', 'VenNom', 'VenEstReg')
        read_only_fields = ('id',)

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ('id', 'CliDNI', 'CliApePat', 'CliNom', 'CliEstReg', 'password', 'username')
        read_only_fields = ('id',) #Campo no se actualiza

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ('id', 'MarNom', 'MarImg', 'MarEstReg')

class TipoArticuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoArticulo
        fields = ('id', 'TipArtNom', 'TipArtEstReg')
        read_only_fields = ('id',)

class ArticuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articulo
        fields = ('id', 'ArtMarCod', 'ArtTipCod', 'ArtNom', 'ArtDes', 'ArtImg', 'ArtSto', 'ArtPreUni', 'ArtEstReg')
        read_only_fields = ('id',)

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = ('id', 'PedCabCodCli', 'PedCabFec', 'PedDetArtCod', 'PedDetEstReg')
        read_only_fields = ('id','PedCabFec',)

    def create_pedido(self, data):
        # Validar los datos enviados en la solicitud
        serializer = PedidoSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        # Obtener los datos validados
        validated_data = serializer.validated_data

        # Obtener el precio del artículo seleccionado
        precio_articulo = validated_data['PedDetArtCod'].ArtPreUni

        # Calcular el subtotal y el total
        subtotal = validated_data['PedDetCantidad'] * precio_articulo
        total = subtotal

        # Agregar el subtotal y el total a los datos validados
        validated_data['PedDetSubtotal'] = subtotal
        validated_data['PedDetTot'] = total

        # Disminuir el stock del artículo correspondiente
        articulo = validated_data['PedDetArtCod']
        cantidad = validated_data['PedDetCantidad']
        articulo.disminuir_stock(cantidad)

        # Crear el pedido
        pedido = Pedido.objects.create(**validated_data)

        return pedido

class CarritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrito
        fields = ('usuario', 'articulo', 'cantidad', 'pedido')