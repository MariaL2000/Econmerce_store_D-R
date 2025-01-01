import json
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Producto

@receiver(post_save, sender=Producto)
def save_product_to_json(sender, instance, created, **kwargs):
    if created:
        # Ruta del archivo JSON
        products_file_path = os.path.join(settings.MEDIA_ROOT, 'products.json')

        # Si el archivo ya existe, cargar los productos existentes
        if os.path.exists(products_file_path):
            with open(products_file_path, 'r') as file:
                products_data = json.load(file)
        else:
            products_data = []

        # Obtener la ruta de la imagen
        imagen_url = instance.imagen.url if instance.imagen else None
        imagen_path = None

        if imagen_url:
            # Se ajusta la ruta a la estructura deseada
            imagen_path = os.path.join('media', imagen_url.lstrip('/'))

        # Agregar el nuevo producto a la lista de productos, incluyendo la imagen
        products_data.append({
            'id': instance.id,
            'nombre': instance.nombre,
            'precio': instance.precio,
            'descripcion': instance.descripcion,
            'stock': instance.stock,
            'imagen': imagen_path,  # Ruta relativa de la imagen
        })

        # Guardar los datos actualizados en el archivo JSON
        with open(products_file_path, 'w') as file:
            json.dump(products_data, file, indent=4)
