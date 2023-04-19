from django.urls import path
from .views import (
    creditoPersonas_create,
    creditoPersonas_listOne,
    creditoPersonas_update,
    creditoPersonas_delete,
    creditoPersonas_list,
    uploadEXCEL_creditosPreaprobados,
    uploadEXCEL_creditosPreaprobados_empleados,
    creditoPersonas_listOne_persona,
    creditoPersonas_listOne_usuario,
    creditoPersonas_lecturaArchivos,
    creditoPersonas_creditoPreaprobado_codigo,
    creditoPersonas_codigo_creditoAprobado,
    creditoPersonas_validar_codigo_creditoAprobado,
    prueba,
)

app_name = 'corp_creditoPersonas'

urlpatterns = [
    path('create/', creditoPersonas_create, name="creditoPersonas_create"),
    path('list/', creditoPersonas_list, name="creditoPersonas_list"),
    path('listOne/<str:pk>', creditoPersonas_listOne, name="creditoPersonas_listOne"),
    path('update/<str:pk>', creditoPersonas_update, name="creditoPersonas_update"),
    path('delete/<str:pk>', creditoPersonas_delete, name="creditoPersonas_delete"),
    path('upload/creditos/preaprobados/', uploadEXCEL_creditosPreaprobados, name="uploadEXCEL_creditosPreaprobados"),
    path('upload/creditos/preaprobados/empleados/', uploadEXCEL_creditosPreaprobados_empleados,
         name="uploadEXCEL_creditosPreaprobados_empleados"),
    path('listOne/persona/<str:pk>', creditoPersonas_listOne_persona, name="creditoPersonas_listOne_persona"),
    path('listOne/usuario/<str:pk>', creditoPersonas_listOne_usuario, name="creditoPersonas_listOne_usuario"),
    path('lecturaArchivos/<str:pk>', creditoPersonas_lecturaArchivos, name="creditoPersonas_lecturaArchivos"),
    path('creditoPreaprobado/codigo', creditoPersonas_creditoPreaprobado_codigo,
         name="creditoPersonas_creditoPreaprobado_codigo"),
    path('generar/codigo/creditoAprobado', creditoPersonas_codigo_creditoAprobado,
         name="creditoPersonas_codigo_creditoAprobado"),
    path('validar/codigo/creditoAprobado', creditoPersonas_validar_codigo_creditoAprobado,
         name="creditoPersonas_validar_codigo_creditoAprobado"),
    path('pruebaConsumer', prueba, name="prueba"),
]
