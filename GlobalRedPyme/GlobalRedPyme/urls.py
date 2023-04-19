"""GlobalRedPyme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    # CORP
    path('corp/empresas/', include(('apps.CORP.corp_empresas.urls', 'empresas'), namespace='empresas')),
    # CENTRAL
    path('core/monedas/', include(('apps.CORE.core_monedas.urls', 'monedas'), namespace='monedas')),
    #MODULO CENTRAL
    path('central/roles/', include(('apps.CENTRAL.central_roles.urls', 'roles'), namespace='roles')),
    path('central/usuarios/', include(('apps.CENTRAL.central_usuarios.urls', 'usuarios'), namespace='usuarios')),
    path('central/auth/', include(('apps.CENTRAL.central_autenticacion.urls', 'autenticacion'), namespace='autenticacion')),
    path('central/acciones/', include(('apps.CENTRAL.central_acciones.urls', 'acciones'), namespace='acciones')),
    path('central/param/', include(('apps.CENTRAL.central_catalogo.urls', 'catalogo'), namespace='catalogo')),
    path('central/facturas/', include(('apps.CENTRAL.central_facturas.urls', 'facturas'), namespace='facturas')),
    url(r'^central/auth/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('central/productos/', include(('apps.CENTRAL.central_productos.urls', 'productos'), namespace='productos')),
    path('central/publicaciones/', include(('apps.CENTRAL.central_publicaciones.urls', 'publicaciones'), namespace='publicaciones')),
    path('central/correosLanding/', include(('apps.CENTRAL.central_correosLanding.urls', 'correosLanding'), namespace='correosLanding')),
    # PERSONAS
    path('personas/personas/', include(('apps.PERSONAS.personas_personas.urls', 'personas'), namespace='personas')),
    path('personas/historialLaboral/', include(('apps.PERSONAS.personas_historialLaboral.urls', 'historialLaboral'), namespace='historialLaboral')),
    path('personas/rucPersonas/', include(('apps.PERSONAS.personas_rucPersonas.urls', 'rucPersonas'), namespace='rucPersonas')),
    path('personas/proveedores/', include(('apps.PERSONAS.personas_proveedores.urls', 'personas_proveedores'), namespace='personas_proveedores')),
    # CORP
    path('corp/cobrarSupermonedas/', include(('apps.CORP.corp_cobrarSupermonedas.urls', 'cobrarSupermonedas'), namespace='cobrarSupermonedas')),
    path('corp/autorizacion/', include(('apps.CORP.corp_autorizaciones.urls', 'autorizacion'), namespace='autorizacion')),
    path('corp/movimientoCobros/', include(('apps.CORP.corp_movimientoCobros.urls', 'movimientoCobros'), namespace='movimientoCobros')),
    path('corp/pagos/', include(('apps.CORP.corp_pagos.urls', 'pagos'), namespace='pagos')),
    path('corp/creditoPersonas/', include(('apps.CORP.corp_creditoPersonas.urls', 'creditoPersonas'), namespace='creditoPersonas')),
    path('corp/creditoPreaprobados/', include(('apps.CORP.corp_creditoPreaprobados.urls', 'creditoPreaprobados'), namespace='creditoPreaprobados')),
    path('corp/notasPedidos/', include(('apps.CORP.corp_notasPedidos.urls', 'corp_notasPedidos'), namespace='corp_notasPedidos')),
    path('corp/monedasEmpresa/', include(('apps.CORP.corp_monedasEmpresa.urls', 'corp_monedasEmpresa'), namespace='corp_monedasEmpresa')),
    path('corp/creditoArchivos/', include(('apps.CORP.corp_creditoArchivos.urls', 'corp_creditoArchivos'), namespace='corp_creditoArchivos')),
    path('corp/envios/', include(('apps.CORP.corp_envios.urls', 'corp_envios'), namespace='corp_envios')),
    path('corp/firmaElectronica/', include(('apps.CORP.corp_firmaElectronica.urls', 'corp_firmaElectronica'), namespace='corp_firmaElectronica')),
    path('corp/pagoProveedores/', include(('apps.CORP.corp_pagoProveedores.urls', 'corp_pagoProveedores'), namespace='corp_pagoProveedores')),
    #Modulo MDM
    path('mdm/prospectosClientes/', include(('apps.MDM.mdm_prospectosClientes.urls', 'prospectos_clientes'), namespace='prospectos_clientes')),
    path('mdm/clientes/', include(('apps.MDM.mdm_clientes.urls', 'clientes'), namespace='clientes')),
    path('mdm/negocios/', include(('apps.MDM.mdm_negocios.urls', 'negocios'), namespace='negocios')),
    path('mdm/facturas/', include(('apps.MDM.mdm_facturas.urls', 'facturasMDM'), namespace='facturasMDM')),
    #Modulo MDP
    path('mdp/categorias/', include(('apps.MDP.mdp_categorias.urls', 'categorias'), namespace='categorias')),
    path('mdp/subCategorias/', include(('apps.MDP.mdp_subCategorias.urls', 'subCategorias'), namespace='subCategorias')),
    path('mdp/productos/', include(('apps.MDP.mdp_productos.urls', 'productosMDP'), namespace='productosMDP')),
    path('mdp/fichaTecnicaProductos/', include(('apps.MDP.mdp_fichaTecnicaProductos.urls', 'fichaTecnicaProductos'), namespace='fichaTecnicaProductos')),
    # Modulo MDO
    path('mdo/prediccionCrosseling/', include(('apps.MDO.mdo_prediccionCrosseling.urls', 'prediccionCrosseling'), namespace='prediccionCrosseling')),
    path('mdo/prediccionRefil/', include(('apps.MDO.mdo_prediccionRefil.urls', 'prediccionRefil'), namespace='prediccionRefil')),
    path('mdo/prediccionProductosNuevos/', include(('apps.MDO.mdo_prediccionProductosNuevos.urls', 'prediccionProductosNuevos'), namespace='prediccionProductosNuevos')),
    path('mdo/generarOferta/', include(('apps.MDO.mdo_generarOferta.urls', 'generarOferta'), namespace='generarOferta')),
    # Modulo GDO
    path('gdo/gestionOferta/', include(('apps.GDO.gdo_gestionOferta.urls', 'gestionOferta'), namespace='gestionOferta')),
    # Modulo GDE
    path('gde/gestionEntrega/', include(('apps.GDE.gde_gestionEntrega.urls', 'gestionEntrega'), namespace='gestionEntrega')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

