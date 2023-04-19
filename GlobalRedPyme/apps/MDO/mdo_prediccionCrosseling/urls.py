from django.urls import path,include
from apps.MDO.mdo_prediccionCrosseling.views import(
	prediccionCrosseling_list, prediccionCrosseling_create, detalles_list, prediccion_crosseling_listOne
)

from rest_framework.authtoken.views import obtain_auth_token

app_name = 'prediccionCrosseling'

urlpatterns = [
	#parametrizaciones	
	path('list/', prediccionCrosseling_list, name="prediccionCrosseling_list"),
	path('create/', prediccionCrosseling_create, name="prediccionCrosseling_create"),
	path('productosImagenes/<int:pk>', detalles_list, name="detalles_list"),
	path('prediccionCrosseling/<int:pk>', prediccion_crosseling_listOne, name="prediccion_crosseling_listOne"),
]
