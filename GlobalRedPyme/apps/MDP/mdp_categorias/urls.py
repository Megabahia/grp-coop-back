from django.urls import path,include

from apps.MDP.mdp_categorias.views import(
	categorias_list, categoria_create, categoria_findOne, categoria_update, categoria_delete,
	buscar_categoria_list, list_categoria_combo
)

from rest_framework.authtoken.views import obtain_auth_token

app_name = 'categorias'

urlpatterns = [
	#CATEGORIAS
	path('list/', categorias_list, name="categorias_list"),
	path('create/', categoria_create, name="categoria_create"),
	path('listOne/<int:pk>', categoria_findOne, name="categoria_findOne"),
	path('update/<int:pk>', categoria_update, name="categoria_update"), 
	path('delete/<int:pk>', categoria_delete, name="categoria_delete"),
	path('listOne/nombre/', buscar_categoria_list, name="buscar_categoria_list"),
	path('list/combo/', list_categoria_combo, name="list_categoria_combo"),
]
