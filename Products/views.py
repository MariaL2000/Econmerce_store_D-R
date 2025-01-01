
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from .models import Producto, Categoria
from .serializers import ProductoSerializer, CategoriaSerializer
from .filters import ProductoFilterView
import os
import json
from django.conf import settings



# Vista para listar productos
class ProductListView(APIView):
    permission_classes=[AllowAny]
    def get(self, request):
        search = request.query_params.get('search', None)
        categoria = request.query_params.get('categoria', None)
        mas_vendidos = request.query_params.get('mas_vendidos', None)

        products = Producto.objects.all()

        if search:
            products = products.filter(nombre__icontains=search)

        if categoria:
            products = products.filter(categoria=categoria)

        if mas_vendidos == 'true':
            products = products.order_by('cantidad_stock')

        serializer = ProductoSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


from pathlib import Path
import json
from django.conf import settings

class ProductCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ProductoSerializer(data=request.data)
        
        if serializer.is_valid():
            producto = serializer.save()  # Guardar el producto en la base de datos
            self.save_product_to_json(producto)  # Llamada a la función con el objeto producto
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def save_product_to_json(self, producto):
        # Datos del producto que quieres guardar
        product_data = {
            'nombre': producto.nombre,
            'descripcion': producto.descripcion,
            'precio': str(producto.precio),  # Convertir el valor Decimal a string
            'precio_descuento': str(producto.precio_descuento),
            'cantidad_stock': producto.cantidad_stock,
            'categoria': producto.categoria,
            'imagen': str(producto.imagen.url) if producto.imagen else None,  # Asegurar que imagen no sea None
        }

        # Usar Path para manejar la ruta del archivo
        file_path = Path(settings.MEDIA_ROOT) / 'productos.json'
        
        # Verificar si el archivo existe y tiene contenido
        try:
            with open(file_path, 'r') as f:
                productos = json.load(f)  # Leer los productos desde el archivo
        except (FileNotFoundError, json.JSONDecodeError):
            productos = []  # Si el archivo no existe o está mal formado, crear una lista vacía
        
        # Añadir el nuevo producto a la lista
        productos.append(product_data)

        # Escribir los productos actualizados en el archivo JSON
        with open(file_path, 'w') as f:
            json.dump(productos, f, indent=4)



# Vista para obtener los detalles de un producto
class ProductDetailView(APIView):
    permission_classes=[AllowAny]
    def get(self, request, pk):
        try:
            # Intentamos obtener el objeto Producto, si no existe lanzamos una excepción
            product = Producto.objects.get(pk=pk)
        except Producto.DoesNotExist:
            # Si el producto no existe, devolvemos una respuesta de error con el código 404
            return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Capturamos cualquier otra excepción que pueda ocurrir
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        # Si el producto existe, serializamos los datos
        serializer = ProductoSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# Vista para actualizar un producto
class ProductUpdateView(APIView):
    permission_classes=[AllowAny]
    def put(self, request, pk):
        product = get_object_or_404(Producto, pk=pk)
        serializer = ProductoSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vista para eliminar un producto
class ProductDeleteView(APIView):
    permission_classes=[AllowAny]
    def delete(self, request, pk):
        product = get_object_or_404(Producto, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Vista para filtrar productos utilizando filters.py
class ProductFilterListView(generics.ListAPIView):
    permission_classes=[AllowAny]
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filterset_class = ProductoFilterView

# Vista para listar categorías
class CategoriaListView(APIView):
    permission_classes=[AllowAny]
    def get(self, request):
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Vista para crear una categoría
class CategoriaCreateView(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vista para obtener detalles de una categoría
class CategoriaDetailView(APIView):
    permission_classes=[AllowAny]
    def get(self, request, pk):
        categoria = get_object_or_404(Categoria, pk=pk)
        serializer = CategoriaSerializer(categoria)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Vista para actualizar una categoría
class CategoriaUpdateView(APIView):
    permission_classes=[AllowAny]
    def put(self, request, pk):
        categoria = get_object_or_404(Categoria, pk=pk)
        serializer = CategoriaSerializer(categoria, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vista para eliminar una categoría
class CategoriaDeleteView(APIView):
    permission_classes=[AllowAny]
    def delete(self, request, pk):
        categoria = get_object_or_404(Categoria, pk=pk)
        categoria.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
