from django.urls import path,include
from apps.PERSONAS.personas_historialLaboral.views import(
	historialLaboral_create,
	historialLaboral_list,
	historialLaboral_listOne,
	historialLaboral_update,
	historialLaboral_delete
)
app_name = 'personas_historialLaboral'

urlpatterns = [
	path('create/', historialLaboral_create, name="historialLaboral_create"),
	path('list/', historialLaboral_list, name="historialLaboral_list"),
	path('listOne/<str:pk>', historialLaboral_listOne, name="historialLaboral_listOne"),
	path('update/<str:pk>', historialLaboral_update, name="historialLaboral_update"),
	path('delete/<str:pk>', historialLaboral_delete, name="historialLaboral_delete"),
]

