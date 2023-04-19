from django.urls import path,include
from apps.MDO.mdo_prediccionProductosNuevos.views import(
	prediccionProductosNuevos_list, prediccionProductosNuevos_create, detalles_list, prediccion_productosNuevos_listOne
)

from rest_framework.authtoken.views import obtain_auth_token

app_name = 'prediccionProductosNuevos'

urlpatterns = [
	#parametrizaciones	
	path('list/', prediccionProductosNuevos_list, name="prediccionProductosNuevos_list"),
	path('create/', prediccionProductosNuevos_create, name="prediccionProductosNuevos_create"),
	path('productosImagenes/<int:pk>', detalles_list, name="detalles_list"),
	path('prediccionProductosNuevos/<int:pk>', prediccion_productosNuevos_listOne, name="prediccion_productosNuevos_listOne"),
]
