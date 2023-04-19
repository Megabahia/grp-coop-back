from django.urls import path,include
from apps.MDO.mdo_prediccionRefil.views import(
	prediccionRefil_list, prediccionRefil_create, detalles_list, prediccion_refil_listOne
)

from rest_framework.authtoken.views import obtain_auth_token

app_name = 'prediccionRefil'

urlpatterns = [
	#parametrizaciones	
	path('list/', prediccionRefil_list, name="prediccionRefil_list"),
	path('create/', prediccionRefil_create, name="prediccionRefil_create"),
	path('productosImagenes/<int:pk>', detalles_list, name="detalles_list"),
	path('prediccionRefil/<int:pk>', prediccion_refil_listOne, name="prediccion_refil_listOne"),
]
