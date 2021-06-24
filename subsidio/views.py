from django.shortcuts import render
from django.shortcuts import render
# Create your views here.
def index(request):
    return render(request,'subsidio/index.html')

def agregar(request):
    return render(request,'subsidio/agregar_beneficio.html')