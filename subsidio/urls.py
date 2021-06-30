from django.conf.urls import include
from django.urls import path
from subsidio.views import *
urlpatterns = [
    path('',index,name="index"),
]