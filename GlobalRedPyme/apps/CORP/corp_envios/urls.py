from django.urls import path
from .views import (
    envios_create,
    envios_list,
)

app_name = 'corp_envios'

urlpatterns = [
    path('create/', envios_create, name="envios_create"),
    path('list/', envios_list, name="envios_list"),
]
