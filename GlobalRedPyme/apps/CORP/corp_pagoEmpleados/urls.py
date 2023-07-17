from django.urls import path,include
from .views import(
	pagoEmpleados_list,
	uploadEXCEL_pagosEmpleados,
	pagoEmpleados_update,
	firmar
)
app_name = 'corp_pagoEmpleados'

urlpatterns = [
	path('list/', pagoEmpleados_list, name="pagoEmpleados_list"),
	path('upload/', uploadEXCEL_pagosEmpleados, name="uploadEXCEL_pagosEmpleados"),
	path('update/<str:pk>', pagoEmpleados_update, name="pagoEmpleados_update"),
	path('firmar/', firmar, name="firmar"),
]

