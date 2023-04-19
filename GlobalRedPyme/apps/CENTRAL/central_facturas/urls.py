from django.urls import path,include
from apps.CENTRAL.central_facturas.views import(
	facturas_create,
	facturas_list,
	facturas_listOne,
	facturas_update,
	facturas_delete,
	facturas_subirArchivo,
)
app_name = 'central_facturas'

urlpatterns = [
	path('subir/factura/', facturas_subirArchivo, name="facturas_subirArchivo"),
	path('create/', facturas_create, name="facturas_create"),
	path('list/', facturas_list, name="facturas_list"),
	path('listOne/<str:pk>', facturas_listOne, name="facturas_listOne"),
	path('update/<str:pk>', facturas_update, name="facturas_update"),
	path('delete/<str:pk>', facturas_delete, name="facturas_delete"),
]

