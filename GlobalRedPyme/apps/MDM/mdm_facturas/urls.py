from django.urls import path
from .views import (
    factura_list, factura_create, factura_findOne, factura_update, factura_delete, factura_list_cliente,
    factura_list_negocio,
    factura_list_rango_fecha_cliente, factura_list_rango_fecha_negocio, factura_list_rango_fecha_cliente_grafica,
    factura_list_rango_fecha_negocio_grafica, factura_list_latest, factura_list_todos_rango_fecha_cliente_grafica,
    factura_list_todos_rango_fecha_negocio_grafica
)

# Esta variable se utiliza para colocar el nombre aplicacion de facturas
app_name = 'facturas'

# La variable urlpatterns se utiliza para exportar las diferentes rutas a las que pueden acceder el front
urlpatterns = [
    # facturas
    path('list/', factura_list, name="factura_list"),
    path('list/negocio/', factura_list_negocio, name="factura_list_negocio"),
    path('list/cliente/', factura_list_cliente, name="factura_list_cliente"),
    path('list/negocio/grafica/', factura_list_todos_rango_fecha_negocio_grafica,
         name="factura_list_todos_rango_fecha_negocio_grafica"),
    path('list/cliente/grafica/', factura_list_todos_rango_fecha_cliente_grafica,
         name="factura_list_todos_rango_fecha_cliente_grafica"),
    path('list/cliente/fecha/<int:pk>', factura_list_rango_fecha_cliente, name="factura_list_rango_fecha_cliente"),
    path('list/negocio/fecha/<int:pk>', factura_list_rango_fecha_negocio, name="factura_list_rango_fecha_negocio"),
    path('list/cliente/fecha/grafica/<int:pk>', factura_list_rango_fecha_cliente_grafica,
         name="factura_list_rango_fecha_cliente_grafica"),
    path('list/negocio/fecha/grafica/<int:pk>', factura_list_rango_fecha_negocio_grafica,
         name="factura_list_rango_fecha_negocio_grafica"),
    path('create/', factura_create, name="factura_create"),
    path('listOne/<int:pk>', factura_findOne, name="factura_findOne"),
    path('listLatest/', factura_list_latest, name="factura_list_latest"),
    # path('update/<int:pk>', factura_update, name="factura_update"),
    # path('delete/<int:pk>', factura_delete, name="factura_delete"),
    # path('upload/csv/', uploadCSV_crearProspectosClientes, name="uploadCSV_crearProspectosClientes"),
    # path('upload/excel/', uploadEXCEL_crearProspectosClientes, name="uploadEXCEL_crearProspectosClientes"),

]
