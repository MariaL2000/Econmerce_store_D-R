import django_filters
from .models import Producto

class ProductoFilterView(django_filters.FilterSet):
    nombre = django_filters.CharFilter(field_name='nombre', lookup_expr='icontains', label='Nombre')
    precio_min = django_filters.NumberFilter(field_name='precio', lookup_expr='gte', label='Precio mínimo')
    precio_max = django_filters.NumberFilter(field_name='precio', lookup_expr='lte', label='Precio máximo')
    mas_vendidos = django_filters.BooleanFilter(method='filter_mas_vendidos', label='Más vendidos')

    class Meta:
        model = Producto
        fields = ['nombre', 'precio_min', 'precio_max']

    def filter_mas_vendidos(self, queryset, name, value):
        # Filtramos productos por más vendidos (esto depende de tu modelo)
        if value:
            return queryset.order_by('-ventas')  # Asumiendo que `ventas` es un campo en el modelo Producto
        return queryset
