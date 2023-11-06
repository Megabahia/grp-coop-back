from django.urls import path, include
from .views.cliente_views import (
    cliente_list, cliente_findOne, cliente_create,
    cliente_update, cliente_delete, clienteImagen_update,
    uploadCSV_crearClientes, uploadEXCEL_crearClientes, cliente_findOne_cedula,
    cliente_by_factura_findOne, cliente_prediccionRefil_findOne,
    cliente_findOne_telefono
)

from .views.datos_fisicos_views import (
    datosFisicos_create, datosFisicos_findOne, datosFisicos_update,
    datosFisicos_delete, datosFisicos_list
)

from .views.datos_virtuales_views import (
    datosVirtuales_create, datosVirtuales_findOne, datosVirtuales_update,
    datosVirtuales_delete, datosVirtuales_list
)

from .views.parientes_views import (
    parientes_create, parientes_findOne, parientes_update,
    parientes_delete, parientes_tabla_list
)

# Esta variable se utiliza para colocar el nombre aplicacion de facturas
app_name = 'clientes'

# La variable urlpatterns se utiliza para exportar las diferentes rutas a las que pueden acceder el front
urlpatterns = [
    # CLIENTES
    path('list/', cliente_list, name="cliente_list"),
    path('create/', cliente_create, name="cliente_create"),
    path('listOne/<int:pk>', cliente_findOne, name="cliente_findOne"),
    path('listOne/cedula/', cliente_findOne_cedula, name="cliente_findOne_cedula"),
    path('listOne/telefono/', cliente_findOne_telefono, name="cliente_findOne_telefono"),
    path('update/<int:pk>', cliente_update, name="cliente_update"),
    path('delete/<int:pk>', cliente_delete, name="cliente_delete"),
    path('update/imagen/<int:pk>', clienteImagen_update, name="clienteImagen_update"),
    path('upload/csv/', uploadCSV_crearClientes, name="uploadCSV_crearClientes"),
    path('upload/excel/', uploadEXCEL_crearClientes, name="uploadEXCEL_crearClientes"),
    path('cliente/factura/<int:pk>', cliente_by_factura_findOne, name="cliente_by_factura_findOne"),
    path('prediccionRefil/listOne/<int:pk>', cliente_prediccionRefil_findOne, name="cliente_prediccionRefil_findOne"),
    # DATOS FISICOS CLIENTE
    path('datos-fisicos-cliente/list/<int:pk>', datosFisicos_list, name="datosFisicos_list"),
    path('datos-fisicos-cliente/create/', datosFisicos_create, name="datosFisicos_create"),
    path('datos-fisicos-cliente/findOne/<int:pk>', datosFisicos_findOne, name="datosFisicos_findOne"),
    path('datos-fisicos-cliente/update/<int:pk>', datosFisicos_update, name="datosFisicos_update"),
    path('datos-fisicos-cliente/delete/<int:pk>', datosFisicos_delete, name="datosFisicos_delete"),
    # DATOS VIRTUALES CLIENTE
    path('datos-virtuales-cliente/list/<int:pk>', datosVirtuales_list, name="datosVirtuales_list"),
    path('datos-virtuales-cliente/create/', datosVirtuales_create, name="datosVirtuales_create"),
    path('datos-virtuales-cliente/findOne/<int:pk>', datosVirtuales_findOne, name="datosVirtuales_findOne"),
    path('datos-virtuales-cliente/update/<int:pk>', datosVirtuales_update, name="datosVirtuales_update"),
    path('datos-virtuales-cliente/delete/<int:pk>', datosVirtuales_delete, name="datosVirtuales_delete"),
    # PARIENTES
    path('parientes-cliente/list/<int:pk>', parientes_tabla_list, name="parientes_tabla_list"),
    path('parientes-cliente/create/', parientes_create, name="parientes_create"),
    path('parientes-cliente/findOne/<int:pk>', parientes_findOne, name="parientes_findOne"),
    path('parientes-cliente/update/<int:pk>', parientes_update, name="parientes_update"),
    path('parientes-cliente/delete/<int:pk>', parientes_delete, name="parientes_delete"),
]
