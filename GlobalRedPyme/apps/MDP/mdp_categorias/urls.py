from django.urls import path, include

from .views import (
    categorias_list, categoria_create, categoria_findOne, categoria_update, categoria_delete,
    buscar_categoria_list, list_categoria_combo
)

# Esta variable se utiliza para colocar el nombre aplicacion de facturas
app_name = 'categorias'

# La variable urlpatterns se utiliza para exportar las diferentes rutas a las que pueden acceder el front
urlpatterns = [
    # CATEGORIAS
    path('list/', categorias_list, name="categorias_list"),
    path('create/', categoria_create, name="categoria_create"),
    path('listOne/<int:pk>', categoria_findOne, name="categoria_findOne"),
    path('update/<int:pk>', categoria_update, name="categoria_update"),
    path('delete/<int:pk>', categoria_delete, name="categoria_delete"),
    path('listOne/nombre/', buscar_categoria_list, name="buscar_categoria_list"),
    path('list/combo/', list_categoria_combo, name="list_categoria_combo"),
]
