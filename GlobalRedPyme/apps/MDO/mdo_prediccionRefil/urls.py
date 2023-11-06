from django.urls import path, include
from .views import (
    prediccionRefil_list, prediccionRefil_create, detalles_list, prediccion_refil_listOne
)

# Esta variable se utiliza para colocar el nombre aplicacion de prediccionCrosseling
app_name = 'prediccionRefil'

# La variable urlpatterns se utiliza para exportar las diferentes rutas a las que pueden acceder el front
urlpatterns = [
    # parametrizaciones
    path('list/', prediccionRefil_list, name="prediccionRefil_list"),
    path('create/', prediccionRefil_create, name="prediccionRefil_create"),
    path('productosImagenes/<int:pk>', detalles_list, name="detalles_list"),
    path('prediccionRefil/<int:pk>', prediccion_refil_listOne, name="prediccion_refil_listOne"),
]
