from django.urls import path, include
from .views import (
    proveedores_create,
    proveedores_listOne,
    proveedores_update,
    proveedores_delete,
    proveedores_list,
)

app_name = 'personas_proveedores'

urlpatterns = [
    path('create/', proveedores_create, name="proveedores_create"),
    path('list/', proveedores_list, name="proveedores_list"),
    path('listOne/<str:pk>', proveedores_listOne, name="proveedores_listOne"),
    path('update/<str:pk>', proveedores_update, name="proveedores_update"),
    path('delete/<str:pk>', proveedores_delete, name="proveedores_delete"),
]
