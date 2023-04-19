from django.urls import path,include

from apps.MDP.mdp_productos.views import (
	productos_list, productos_create, productos_findOne, productos_update, productos_delete,
	producto_images_findOne,
	search_producto_list, abastecimiento_list, stock_list, caducidad_list, rotacion_list, refil_list,
	abastecimiento_create,
	uploadEXCEL_crearProductos, productoImagen_list, prediccion_crosseling_list,
	producto_refil_list, prediccion_refil_list, prediccion_productosNuevos_list,
	search_producto_codigo_list, producto_images_delete
)

from rest_framework.authtoken.views import obtain_auth_token

app_name = 'productos'

urlpatterns = [
	#PRODUCTOS
	path('list/', productos_list, name="productos_list"),
	path('create/', productos_create, name="productos_create"),
	path('listOne/<int:pk>', productos_findOne, name="productos_findOne"), 
	path('update/<int:pk>', productos_update, name="productos_update"), 
	path('delete/<int:pk>', productos_delete, name="productos_delete"),
	path('search/producto/', search_producto_list, name="search_producto_list"),
	path('search/producto/codigo/', search_producto_codigo_list, name="search_producto_codigo_list"),
	path('upload/excel/', uploadEXCEL_crearProductos, name="uploadEXCEL_crearProductos"),
	# IMAGENES PRODUCTOS
	path('imagen/<int:pk>', producto_images_findOne, name="producto_images_findOne"), 
	path('imagen/delete/<int:pk>', producto_images_delete, name="producto_images_delete"), 
	# REPORTE ABASTECIMIENTO
	path('abastecimiento/create/', abastecimiento_create, name="abastecimiento_create"),
	path('abastecimiento/list/', abastecimiento_list, name="abastecimiento_list"),
	# REPORTE STOCK
	path('stock/list/', stock_list, name="stock_list"),
	# REPORTE CADUCIDAD
	path('caducidad/list/', caducidad_list, name="caducidad_list"),
	# REPORTE ROTACION
	path('rotacion/list/', rotacion_list, name="rotacion_list"),
	# REPORTE REFIL
	path('refil/list/', refil_list, name="refil_list"),
	# OBTENER URL IMAGEN
	path('producto/image/', productoImagen_list, name="productoImagen_list"),
	# OBTENER PREDICCION CROSSELING
	path('prediccionCrosseling/', prediccion_crosseling_list, name="prediccion_crosseling_list"),
	# OBTENER REFIL PRODUCTO
	path('producto/refil/', producto_refil_list, name="producto_refil_list"),
	# OBTENER PREDICCION REFIL
	path('prediccionRefil/', prediccion_refil_list, name="prediccion_refil_list"),
	# OBTENER PREDICCION PRODUCTOS NUEVOS
	path('prediccionProductosNuevos/', prediccion_productosNuevos_list, name="prediccion_productosNuevos_list"),
]
