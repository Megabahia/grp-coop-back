from django.urls import path,include
from apps.MDM.mdm_negocios.views.negocio_views import(
	negocio_list, negocio_findOne, negocio_create,
	negocio_update, negocio_delete, negociosImagen_update, negocio_findOne_ruc, negocio_by_factura_findOne,
	negocio_prediccionRefil_findOne, negocio_findOne_telefonoOficina
)
from apps.MDM.mdm_negocios.views.direccion_establecimiento_views import(
	direccionesNegocio_list, direccionesNegocio_findOne, direccionesNegocio_create,
	direccionesNegocio_update, direccionesNegocio_delete
)
from apps.MDM.mdm_negocios.views.personal_views import(
	personalNegocios_list, personalNegocios_findOne, personalNegocios_create,
	personalNegocios_update, personalNegocios_delete
)

from rest_framework.authtoken.views import obtain_auth_token

app_name = 'negocios'

urlpatterns = [
	# NEGOCIO
	path('list/', negocio_list, name="negocio_list"),
	path('create/', negocio_create, name="negocio_create"),
	path('listOne/<int:pk>', negocio_findOne, name="negocio_findOne"), 
	path('listOne/ruc/', negocio_findOne_ruc, name="negocio_findOne_ruc"), 
	path('listOne/telefonoOficina/', negocio_findOne_telefonoOficina, name="negocio_findOne_telefonoOficina"), 
	path('update/<int:pk>', negocio_update, name="negocio_update"), 
	path('delete/<int:pk>', negocio_delete, name="negocio_delete"),
	path('update/imagen/<int:pk>', negociosImagen_update, name="negociosImagen_update"),	
	path('negocio/factura/<int:pk>', negocio_by_factura_findOne, name="negocio_by_factura_findOne"),	
	path('prediccionRefil/listOne/<int:pk>', negocio_prediccionRefil_findOne, name="negocio_prediccionRefil_findOne"), 
    # DIREECIONES ESTABLECIMIENTOS
    path('direcciones/list/<int:pk>', direccionesNegocio_list, name="direccionesNegocio_list"),
	path('direcciones/create/', direccionesNegocio_create, name="direccionesNegocio_create"),
	path('direcciones/listOne/<int:pk>', direccionesNegocio_findOne, name="direccionesNegocio_findOne"), 
	path('direcciones/update/<int:pk>', direccionesNegocio_update, name="direccionesNegocio_update"), 
	path('direcciones/delete/<int:pk>', direccionesNegocio_delete, name="direccionesNegocio_delete"),
    # PERSONAL
    path('personal/list/<int:pk>', personalNegocios_list, name="personalNegocios_list"),
	path('personal/create/', personalNegocios_create, name="personalNegocios_create"),
	path('personal/listOne/<int:pk>', personalNegocios_findOne, name="personalNegocios_findOne"), 
	path('personal/update/<int:pk>', personalNegocios_update, name="personalNegocios_update"), 
	path('personal/delete/<int:pk>', personalNegocios_delete, name="personalNegocios_delete"),
]
