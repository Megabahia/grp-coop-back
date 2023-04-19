from django.urls import path
from .views import (
    cobrarSupermonedas_create,
    cobrarSupermonedas_list,
    cobrarSupermonedas_listOne,
    cobrarSupermonedas_update,
    cobrarSupermonedas_delete,
    cobrarSupermonedas_search,
)

app_name = 'corp_cobrarSupermonedas'

urlpatterns = [
    path('create/', cobrarSupermonedas_create, name="cobrarSupermonedas_create"),
    path('list/', cobrarSupermonedas_list, name="cobrarSupermonedas_list"),
    path('search/', cobrarSupermonedas_search, name="cobrarSupermonedas_search"),
    path('listOne/<str:pk>', cobrarSupermonedas_listOne, name="cobrarSupermonedas_listOne"),
    path('update/<str:pk>', cobrarSupermonedas_update, name="cobrarSupermonedas_update"),
    path('delete/<str:pk>', cobrarSupermonedas_delete, name="cobrarSupermonedas_delete"),
]
