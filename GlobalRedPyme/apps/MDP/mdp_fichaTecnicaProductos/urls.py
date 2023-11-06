from django.urls import path

from .views import (
    fichaTecnicaProductos_list, fichaTecnicaProductos_create, fichaTecnicaProductos_findOne,
    fichaTecnicaProductos_update, fichaTecnicaProductos_delete
)

# Esta variable se utiliza para colocar el nombre aplicacion de fichaTecnicaProductos
app_name = 'fichaTecnicaProductos'

# La variable urlpatterns se utiliza para exportar las diferentes rutas a las que pueden acceder el front
urlpatterns = [
    # FICHA TECNICA
    path('list/<int:pk>', fichaTecnicaProductos_list, name="fichaTecnicaProductos_list"),
    path('create/', fichaTecnicaProductos_create, name="fichaTecnicaProductos_create"),
    path('listOne/<int:pk>', fichaTecnicaProductos_findOne, name="fichaTecnicaProductos_findOne"),
    path('update/<int:pk>', fichaTecnicaProductos_update, name="fichaTecnicaProductos_update"),
    path('delete/<int:pk>', fichaTecnicaProductos_delete, name="fichaTecnicaProductos_delete"),
]
