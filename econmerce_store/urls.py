from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token  # Importar la vista de obtención del token


urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta del admin de Django
    path('products/', include('Products.urls')),
    path('Car_list/', include('Car_list.urls')), 
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('Users/', include('Users.urls')),  # Incluye las URLs de la app Users
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
