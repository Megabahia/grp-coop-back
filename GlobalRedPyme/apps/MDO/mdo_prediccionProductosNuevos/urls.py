from django.urls import path
from .views import (
    prediccionProductosNuevos_list, prediccionProductosNuevos_create, detalles_list, prediccion_productosNuevos_listOne
)

# Esta variable se utiliza para colocar el nombre aplicacion de facturas
app_name = 'prediccionProductosNuevos'

# La variable urlpatterns se utiliza para exportar las diferentes rutas a las que pueden acceder el front
urlpatterns = [
    # parametrizaciones
    path('list/', prediccionProductosNuevos_list, name="prediccionProductosNuevos_list"),
    path('create/', prediccionProductosNuevos_create, name="prediccionProductosNuevos_create"),
    path('productosImagenes/<int:pk>', detalles_list, name="detalles_list"),
    path('prediccionProductosNuevos/<int:pk>', prediccion_productosNuevos_listOne,
         name="prediccion_productosNuevos_listOne"),
]
