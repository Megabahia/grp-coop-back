from django.urls import path,include
from apps.CENTRAL.central_correosLanding.views import(
	correos_create,
	correos_list,
	correos_update,
)
app_name = 'central_correosLanding'

urlpatterns = [
	path('create/', correos_create, name="correos_create"),
	path('list/', correos_list, name="correos_list"),
	path('update/<str:pk>', correos_update, name="correos_update"),
]

