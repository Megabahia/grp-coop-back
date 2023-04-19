from django.urls import path
from .views import (
    monedas_create,
    monedas_list,
    monedas_listOne,
    monedas_update,
    monedas_delete,
    monedas_usuario,
    monedas_listOtorgadas,
    uploadEXCEL_monedasRegaladas,
    uploadEXCEL_monedasRegaladasClientes,
    list_monedas_regaladas_empresa,
)

app_name = 'core_monedas'

urlpatterns = [
    path('create/', monedas_create, name="monedas_create"),
    path('list/', monedas_list, name="monedas_list"),
    path('listOne/<str:pk>', monedas_listOne, name="monedas_listOne"),
    path('update/<str:pk>', monedas_update, name="monedas_update"),
    path('delete/<str:pk>', monedas_delete, name="monedas_delete"),
    path('usuario/<str:pk>', monedas_usuario, name="monedas_usuario"),
    path('list/otorgadas/', monedas_listOtorgadas, name="monedas_listOtorgadas"),
    path('upload/monedas', uploadEXCEL_monedasRegaladas, name="uploadEXCEL_monedasRegaladas"),
    path('upload/monedasClientes', uploadEXCEL_monedasRegaladasClientes, name="uploadEXCEL_monedasRegaladasClientes"),
    path('list/monedas/empresas', list_monedas_regaladas_empresa, name="list_monedas_regaladas_empresa"),
]
