from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Productos
    path('', views.ProductListView.as_view(), name='product-list'),
    path('crear/', views.ProductCreateView.as_view(), name='product-create'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('<int:pk>/actualizar/', views.ProductUpdateView.as_view(), name='product-update'),
    path('<int:pk>/eliminar/', views.ProductDeleteView.as_view(), name='product-delete'),
    path('filtrar/', views.ProductFilterListView.as_view(), name='product-filter'),

    # Categorías
    path('categorias/', views.CategoriaListView.as_view(), name='categoria-list'),
    path('categorias/crear/', views.CategoriaCreateView.as_view(), name='categoria-create'),
    path('categorias/<int:pk>/', views.CategoriaDetailView.as_view(), name='categoria-detail'),
    path('categorias/<int:pk>/actualizar/', views.CategoriaUpdateView.as_view(), name='categoria-update'),
    path('categorias/<int:pk>/eliminar/', views.CategoriaDeleteView.as_view(), name='categoria-delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

