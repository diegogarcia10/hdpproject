from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from django.http import HttpResponse,JsonResponse
from django.core import serializers
import json
# Create your views here.
def index(request):
    return render(request,'subsidio/index.html')

def agregar(request):
    err=""
    if request.method=='POST':
        cantidad=request.POST.get('cantidad',False)
        id_tipoSubsidio=request.POST.get('id_tipoSubsidio',False)
        print(id_tipoSubsidio)
        
        subsidios=TipoSubsidio.objects.all()
        contexto={'cantidad':cantidad,
                  'subsidios':subsidios,
                  'id_tipoSubsidio' : id_tipoSubsidio,
            }
        
        if(cantidad=="" or id_tipoSubsidio==""):
            err="Complete todos los campos por favor"
            contexto['err']=err
            return render(request,'subsidio/agregar_beneficio.html',contexto)
        
        modelo_beneficio=BeneficiarioTipoSubsidio() 

        usuario_logueado = User.objects.get(username=request.user)
        print(usuario_logueado)
        
        beneficiario_logueado = Beneficiario.objects.get(codigo_usuario=usuario_logueado)
        print(beneficiario_logueado)
        
        tiposubsidio_cod=TipoSubsidio.objects.get(id=id_tipoSubsidio)
        modelo_beneficio.codigo_subsidio=tiposubsidio_cod
        
        modelo_beneficio.codigo_beneficiario=beneficiario_logueado
        
        modelo_beneficio.cantidad = cantidad
        
        modelo_beneficio.save()
        messages.success(request, "Beneficio agregado correctamente")
    

    subsidios=TipoSubsidio.objects.all()
    print(subsidios)
    return render(request,'subsidio/agregar_beneficio.html',{'subsidios':subsidios,'err':err}) 


def municipios(request):
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("""SELECT SUM(subsidio_beneficiariotiposubsidio.cantidad),subsidio_tiposubsidio.nombre_tipo_subsidio, subsidio_municipio.nombre_municipio 
                       FROM subsidio_beneficiariotiposubsidio 
                       INNER JOIN subsidio_tiposubsidio ON subsidio_tiposubsidio.id=subsidio_beneficiariotiposubsidio.codigo_subsidio_id 
                       INNER JOIN subsidio_beneficiario ON subsidio_beneficiario.id=subsidio_beneficiariotiposubsidio.codigo_beneficiario_id 
                       INNER JOIN subsidio_municipio ON subsidio_municipio.id=subsidio_beneficiario.codigo_municipio_id 
                       GROUP BY subsidio_municipio.nombre_municipio, subsidio_tiposubsidio.nombre_tipo_subsidio""")
        rawData = cursor.fetchall()
        result = []
        for r in rawData:
            result.append(list(r))
            contexto={'municipios': result }
            print(contexto)
    return render(request,'subsidio/consulta_municipios.html',contexto)

def departamentos(request):
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("""SELECT SUM(subsidio_beneficiariotiposubsidio.cantidad), subsidio_tiposubsidio.nombre_tipo_subsidio, subsidio_departamento.nombre_departamento  
                       FROM subsidio_beneficiariotiposubsidio 
                       INNER JOIN subsidio_tiposubsidio ON subsidio_tiposubsidio.id=subsidio_beneficiariotiposubsidio.codigo_subsidio_id 
                       INNER JOIN subsidio_beneficiario ON subsidio_beneficiario.id=subsidio_beneficiariotiposubsidio.codigo_beneficiario_id
                       INNER JOIN subsidio_municipio ON subsidio_municipio.id=subsidio_beneficiario.codigo_municipio_id
                       INNER JOIN subsidio_departamento ON subsidio_departamento.id=subsidio_municipio.codigo_departamento_id
                       GROUP BY subsidio_departamento.nombre_departamento, subsidio_tiposubsidio.nombre_tipo_subsidio""")
        rawData = cursor.fetchall()
        result = []
        for r in rawData:
            result.append(list(r))
            contexto={'departamentos': result }
            print(contexto)
    return render(request,'subsidio/consulta_departamentos.html',contexto)

def zonas(request):
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("""SELECT subsidio_zona.nombre_zona, subsidio_tiposubsidio.nombre_tipo_subsidio, TRUNCATE(SUM(subsidio_beneficiariotiposubsidio.cantidad),2) 
                       FROM subsidio_beneficiariotiposubsidio 
                       INNER JOIN subsidio_tiposubsidio ON subsidio_tiposubsidio.id=subsidio_beneficiariotiposubsidio.codigo_subsidio_id  
                       INNER JOIN subsidio_beneficiario ON subsidio_beneficiario.id=subsidio_beneficiariotiposubsidio.codigo_beneficiario_id
                       INNER JOIN subsidio_municipio ON subsidio_municipio.id=subsidio_beneficiario.codigo_municipio_id
                       INNER JOIN subsidio_departamento ON subsidio_departamento.id=subsidio_municipio.codigo_departamento_id
                       INNER JOIN subsidio_zona ON subsidio_zona.id=subsidio_departamento.codigo_zona_id
                       GROUP BY subsidio_zona.nombre_zona, subsidio_tiposubsidio.nombre_tipo_subsidio""")
        rawData = cursor.fetchall()        
        result = []
        for r in rawData:
            result.append(list(r))
            contexto={'zonas': result}
            print(contexto)
    zonas2=Zona.objects.raw('select subsidio_zona.*, sum(subsidio_beneficiariotiposubsidio.cantidad) as cantidad from subsidio_zona inner join subsidio_departamento on subsidio_zona.id=subsidio_departamento.codigo_zona_id inner JOIN subsidio_municipio on subsidio_departamento.id=subsidio_municipio.codigo_departamento_id inner join subsidio_beneficiario on subsidio_municipio.id=subsidio_beneficiario.codigo_municipio_id inner join subsidio_beneficiariotiposubsidio on subsidio_beneficiario.id=subsidio_beneficiariotiposubsidio.codigo_beneficiario_id GROUP BY subsidio_zona.nombre_zona;')
    labels = []
    data = []
    for x in zonas2:
        labels.append(x.nombre_zona)
        data.append(str(x.cantidad))
    contexto['labels']=labels
    contexto['data']=data    
    return render(request,'subsidio/consulta_zonas.html',contexto)

def suma_zonas(request):
    zonas2=Zona.objects.raw('select subsidio_zona.nombre_zona, sum(subsidio_beneficiariotiposubsidio.cantidad) as cantidad from subsidio_zona inner join subsidio_departamento on subsidio_zona.id=subsidio_departamento.codigo_zona_id inner JOIN subsidio_municipio on subsidio_departamento.id=subsidio_municipio.codigo_departamento_id inner join subsidio_beneficiario on subsidio_municipio.id=subsidio_beneficiario.codigo_municipio_id inner join subsidio_beneficiariotiposubsidio on subsidio_beneficiario.id=subsidio_beneficiariotiposubsidio.codigo_beneficiario_id GROUP BY subsidio_zona.nombre_zona;')
    labels = []
    data = []
    for x in zonas2:
        labels.append(x.nombre_zona)
        data.append(x.cantidad)   
        
    