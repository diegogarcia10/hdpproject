from django.conf.urls import include
from django.urls import path
from subsidio.views import *
urlpatterns = [
    path('',index,name="index"),
    path('suma_zonas',suma_zonas,name="suma_zonas")
]