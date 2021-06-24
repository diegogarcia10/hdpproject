from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import *
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
    

    subsidios=TipoSubsidio.objects.all()
    print(subsidios)
    return render(request,'subsidio/agregar_beneficio.html',{'subsidios':subsidios,'err':err}) 

def municipios(request):
    municipios=BeneficiarioTipoSubsidio.objects.all()
    
    return render(request,'subsidio/consulta_municipios.html',{'municipios': municipios})