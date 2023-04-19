from django.urls import path,include

from apps.MDP.mdp_fichaTecnicaProductos.views import(
	fichaTecnicaProductos_list, fichaTecnicaProductos_create, fichaTecnicaProductos_findOne, fichaTecnicaProductos_update, fichaTecnicaProductos_delete
)

from rest_framework.authtoken.views import obtain_auth_token

app_name = 'fichaTecnicaProductos'

urlpatterns = [
	#FICHA TECNICA
	path('list/<int:pk>', fichaTecnicaProductos_list, name="fichaTecnicaProductos_list"),
	path('create/', fichaTecnicaProductos_create, name="fichaTecnicaProductos_create"),
	path('listOne/<int:pk>', fichaTecnicaProductos_findOne, name="fichaTecnicaProductos_findOne"), 
	path('update/<int:pk>', fichaTecnicaProductos_update, name="fichaTecnicaProductos_update"), 
	path('delete/<int:pk>', fichaTecnicaProductos_delete, name="fichaTecnicaProductos_delete"),
]
