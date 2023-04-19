from django.urls import path,include
from .views import(
	personas_create,
	personas_listOne,
	personas_update,
	personas_delete,
	personas_imagenUpdate,
	personas_validarCodigo,
	personas_update_sin_imagen,
	personas_listOne_cedula,
	personas_update_empresa,
)
app_name = 'personas_personas'

urlpatterns = [
	path('create/', personas_create, name="personas_create"),
	path('listOne/<str:pk>', personas_listOne, name="personas_listOne"),
	path('update/<str:pk>', personas_update, name="personas_update"),
	path('updateSinImagen/<str:pk>', personas_update_sin_imagen, name="personas_update_sin_imagen"),
	path('delete/<str:pk>', personas_delete, name="personas_delete"),
	path('update/imagen/<str:pk>', personas_imagenUpdate, name="personas_imagenUpdate"),
	path('validarCodigo/', personas_validarCodigo, name="personas_validarCodigo"),
	path('listOne/cedula/', personas_listOne_cedula, name="personas_listOne_cedula"),
	path('infoEmpresa/<str:pk>', personas_update_empresa, name="personas_update_empresa"),
]

