from rest_framework import serializers
from .models import Carrito, CarritoProducto, Orden

class CarritoProductoSerializer(serializers.ModelSerializer):
    producto_detalle = serializers.StringRelatedField(source='producto', read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CarritoProducto
        fields = ['id', 'carrito', 'producto', 'producto_detalle', 'cantidad', 'subtotal']

    def get_subtotal(self, obj):
        return obj.subtotal()

class CarritoSerializer(serializers.ModelSerializer):
    productos = CarritoProductoSerializer(source='carritoproducto_set', many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Carrito
        fields = ['id', 'usuario', 'productos', 'total']

    def get_total(self, obj):
        return obj.total()

class OrdenSerializer(serializers.ModelSerializer):
    carrito = CarritoSerializer(read_only=True)

    class Meta:
        model = Orden
        fields = ['id', 'usuario', 'carrito', 'fecha', 'total']