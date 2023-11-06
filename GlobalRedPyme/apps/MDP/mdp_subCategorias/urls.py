from django.urls import path

from .views import (
    subCategorias_list, subCategoria_create, subCategoria_findOne, subCategoria_update, subCategoria_delete,
    list_subcategorias_padre_combo
)

# Esta variable se utiliza para colocar el nombre aplicacion de subCategorias
app_name = 'subCategorias'

# La variable urlpatterns se utiliza para exportar las diferentes rutas a las que pueden acceder el front
urlpatterns = [
    # SUBCATEGORIAS
    path('list/', subCategorias_list, name="subCategorias_list"),
    path('create/', subCategoria_create, name="subCategoria_create"),
    path('listOne/<int:pk>', subCategoria_findOne, name="subCategoria_findOne"),
    path('update/<int:pk>', subCategoria_update, name="subCategoria_update"),
    path('delete/<int:pk>', subCategoria_delete, name="subCategoria_delete"),
    # BUSCAR SUBCATEGORIAS DEL PADRE
    path('list/<int:pk>', list_subcategorias_padre_combo, name="list_subcategorias_padre_combo"),
]
