"""ProyectoStarWash URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,include
# Ubicacion de un directorio statico
from django.conf.urls.static import static
# Importar el archivo de "settings" (las variables MEDIA)
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('StarWash.urls')), # si no se escribe nada cargara las rutas del proyecto
    path('',include('api.urls')), # si no se escribe nada cargara las rutas de api
    path('', include('pwa.urls')), # incuye la apicacion pwa
]
# Incluir en el Path el directorio "MEDIA" (el nombre y la ruta)
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

admin.site.site_header="Panel Administración Star Wash"
admin.site.index_title="Modulos de Administración Star Wash"
admin.site.site_title="Star Wash"