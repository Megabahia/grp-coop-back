from django.urls import path
from .views import (
    firmaElectronica_create,
    firmaElectronica_list,
)

app_name = 'corp_monedasEmpresa'

urlpatterns = [
    path('create/', firmaElectronica_create, name="firmaElectronica_create"),
    path('list/', firmaElectronica_list, name="firmaElectronica_list"),
]
