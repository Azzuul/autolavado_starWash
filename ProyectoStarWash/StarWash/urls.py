from django.contrib import admin
from django.urls import path,include
from .views import index,galeria,formulario,contacto,conocenos,ubicacion, insumos, login, logout_vista, adminInsumo, eliminar_insumo, buscar, modificar,guardar_token

urlpatterns = [
    path('',index,name="INDEX"),
    path('galeria/',galeria,name="GALERIA"),
    path('formulario/',formulario,name="FORMULARIO"),
    path('contacto/',contacto,name='CONTACTO'),
    path('conocenos/',conocenos,name="CONOCENOS"),
    path('ubicacion/',ubicacion,name="UBICACION"),
    path('registro_insumos/', insumos, name='INSUMOS'),
    path('login/', login, name="LOGIN"),
    path('logout_vista/', logout_vista, name="LOGOUT"),
    path('administracion_insumos/', adminInsumo, name='ADMIN_INSUMO'),
    path('eliminar_insumo/<id>/', eliminar_insumo, name="ELIM_INSUMO"),
    path('buscar/<id>/', buscar, name='BUSCAR'),
    path('modificar/', modificar, name='MODIFICAR'),
    path('oauth/', include('social_django.urls', namespace='social')), # Incluye el paquete de social django para facebook
    path('guardar-token/',guardar_token,name='guardar-token'),
]
