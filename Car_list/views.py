from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Carrito, CarritoProducto, Orden
from .serializers import CarritoSerializer, CarritoProductoSerializer, OrdenSerializer
from Products.models import Producto
from rest_framework.permissions import IsAuthenticated


class CarritoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]  # Requiere autenticación
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer

    def get_queryset(self):
        # Filtra los carritos por el usuario autenticado
        return self.queryset.filter(usuario=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        carrito = self.get_object()
        serializer = self.get_serializer(carrito)
        total = carrito.total()  # Calcula el total del carrito
        return Response({
            'carrito': serializer.data,
            'total': total
        })

    @action(detail=True, methods=['post'], url_path='add-product')
    def add_product(self, request, pk=None):
        carrito = self.get_object()
        producto_id = request.data.get('producto_id')
        cantidad = request.data.get('cantidad', 1)

        if not producto_id or not isinstance(cantidad, int) or cantidad <= 0:
            return Response({'error': 'Datos inválidos'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            producto = Producto.objects.get(id=producto_id)
            carrito_producto, created = CarritoProducto.objects.get_or_create(carrito=carrito, producto=producto)
            if not created:
                carrito_producto.cantidad += cantidad
            else:
                carrito_producto.cantidad = cantidad
            carrito_producto.save()
            return Response({'detail': 'Producto añadido al carrito'}, status=status.HTTP_200_OK)
        except Producto.DoesNotExist:
            return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], url_path='remove-product')
    def remove_product(self, request, pk=None):
        carrito = self.get_object()
        producto_id = request.data.get('producto_id')

        if not producto_id:
            return Response({'error': 'ID de producto no proporcionado'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            producto = Producto.objects.get(id=producto_id)
            carrito_producto = CarritoProducto.objects.get(carrito=carrito, producto=producto)
            carrito_producto.delete()
            return Response({'detail': 'Producto eliminado del carrito'}, status=status.HTTP_200_OK)
        except (Producto.DoesNotExist, CarritoProducto.DoesNotExist):
            return Response({'error': 'Producto no encontrado en el carrito'}, status=status.HTTP_404_NOT_FOUND)


class OrdenViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]  # Requiere autenticación
    queryset = Orden.objects.all()
    serializer_class = OrdenSerializer

    def get_queryset(self):
        # Filtra las órdenes por el usuario autenticado
        return self.queryset.filter(usuario=self.request.user)

    def create(self, request, *args, **kwargs):
        carrito_id = request.data.get('carrito_id')

        if not carrito_id:
            return Response({'error': 'ID de carrito no proporcionado'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            carrito = Carrito.objects.get(id=carrito_id, usuario=request.user)
            if not carrito.carritoproducto_set.exists():
                return Response({'error': 'El carrito está vacío'}, status=status.HTTP_400_BAD_REQUEST)

            total = carrito.total()  # Asegúrate de que este método esté implementado en el modelo Carrito
            orden = Orden.objects.create(usuario=request.user, carrito=carrito, total=total)
            return Response(OrdenSerializer(orden).data, status=status.HTTP_201_CREATED)
        except Carrito.DoesNotExist:
            return Response({'error': 'Carrito no encontrado'}, status=status.HTTP_404_NOT_FOUND)
