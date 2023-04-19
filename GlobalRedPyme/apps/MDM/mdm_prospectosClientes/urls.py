from django.urls import path,include
from apps.MDM.mdm_prospectosClientes.views import(
	prospecto_cliente_list, prospecto_cliente_findOne, prospecto_cliente_create,
	prospecto_cliente_update, prospecto_cliente_delete, prospectosclientesImagen_update,
	uploadCSV_crearProspectosClientes,uploadEXCEL_crearProspectosClientes, prospecto_cliente_search
)

from rest_framework.authtoken.views import obtain_auth_token

app_name = 'prospectos_clientes'

urlpatterns = [
	#parametrizaciones
	path('list/', prospecto_cliente_list, name="prospecto_cliente_list"),
	path('search/', prospecto_cliente_search, name="prospecto_cliente_search"),
	path('create/', prospecto_cliente_create, name="prospecto_cliente_create"),
	path('listOne/<int:pk>', prospecto_cliente_findOne, name="prospecto_cliente_findOne"), 
	path('update/<int:pk>', prospecto_cliente_update, name="prospecto_cliente_update"), 
	path('delete/<int:pk>', prospecto_cliente_delete, name="prospecto_cliente_delete"),	
	path('update/imagen/<int:pk>', prospectosclientesImagen_update, name="prospectosclientesImagen_update"),
	path('upload/csv/', uploadCSV_crearProspectosClientes, name="uploadCSV_crearProspectosClientes"),
	path('upload/excel/', uploadEXCEL_crearProspectosClientes, name="uploadEXCEL_crearProspectosClientes"),		
	
]
