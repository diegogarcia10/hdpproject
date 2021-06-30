"""subsidioproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib.auth.decorators import login_required
from usuario.views import *
from subsidio.views import *

urlpatterns = [
    path('admin/', admin.site.urls,name='admin'),
    path('',include('subsidio.urls')),
    path('accounts/login/',login, name="login"),
    path('logout/',logout_v, name='logout'),
    path('registro/',registro,name="registro"),
    path('agregar/',login_required(agregar),name="agregar"),
    path('consulta_municipios/',municipios,name="municipios"),
    path('consulta_departamentos/',departamentos,name="departamentos"),
    path('consulta_zonas/',zonas,name="zonas")
]
