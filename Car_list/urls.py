from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CarritoViewSet, OrdenViewSet

# Usando DefaultRouter para rutas automáticas
router = DefaultRouter()
router.register(r'carrito', CarritoViewSet, basename='carrito')
router.register(r'orden', OrdenViewSet, basename='orden')

urlpatterns = router.urls
