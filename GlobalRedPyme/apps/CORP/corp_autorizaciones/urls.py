from django.urls import path, include
from .views import (
    autorizacion_create,
    autorizacion_list,
    autorizacion_listOne,
    autorizacion_update,
    autorizacion_delete
)

app_name = 'corp_autorizaciones'

urlpatterns = [
    path('create/', autorizacion_create, name="autorizacion_create"),
    path('list/', autorizacion_list, name="autorizacion_list"),
    path('listOne/<str:pk>', autorizacion_listOne, name="autorizacion_listOne"),
    path('update/<str:pk>', autorizacion_update, name="autorizacion_update"),
    path('delete/<str:pk>', autorizacion_delete, name="autorizacion_delete"),
]
