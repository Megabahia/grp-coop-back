from django.urls import path
from .views import (
    prediccionCrosseling_list, prediccionCrosseling_create, detalles_list, prediccion_crosseling_listOne
)

# Esta variable se utiliza para colocar el nombre aplicacion de prediccionCrosseling
app_name = 'prediccionCrosseling'

# La variable urlpatterns se utiliza para exportar las diferentes rutas a las que pueden acceder el front
urlpatterns = [
    # parametrizaciones
    path('list/', prediccionCrosseling_list, name="prediccionCrosseling_list"),
    path('create/', prediccionCrosseling_create, name="prediccionCrosseling_create"),
    path('productosImagenes/<int:pk>', detalles_list, name="detalles_list"),
    path('prediccionCrosseling/<int:pk>', prediccion_crosseling_listOne, name="prediccion_crosseling_listOne"),
]
