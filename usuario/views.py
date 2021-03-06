from django.db.models.query import RawQuerySet
from django.shortcuts import render,redirect,reverse
from django.contrib.auth import authenticate,logout, login as lg
from subsidio.models import *
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

# Create your views here.
def login(request):
	if request.user.is_authenticated:
		return redirect('index')
	else:
		err=""
		if request.method=='POST':
			username=request.POST.get('username',False)
			password=request.POST.get('password',False)
			user=authenticate(request,username=username,password=password)
			if user is not None:
				lg(request,user)
				if(user.is_superuser):
					return HttpResponseRedirect(reverse('admin:index'))
				return redirect('agregar')
			else:
				err="Error al ingresar las credenciales, asegurese  que el usuario y contraseña esten correctamente escritos"
				return render(request,'auth/login.html',{'err':err,'username':username})
		else:
			return render(request,'auth/login.html')
	


def logout_v(request):
    logout(request)
    return redirect('index')

def registro(request):
	err = ""
	if request.method == 'POST':
		username = request.POST.get('username', False)
		nombre = request.POST.get('first_name', False)
		apellido = request.POST.get('last_name', False)
		dui = request.POST.get('dui', False)
		nit = request.POST.get('nit', False)
		email = request.POST.get('email', False)
		id_municipio = request.POST.get('id_municipio', False)
		password1 = request.POST.get('password1', False)
		password2 = request.POST.get('password2', False)
		es_empresa = request.POST.get('es_empresa', False)
		es_persona_natural = request.POST.get('es_persona_natural', False)
		print(id_municipio)

		municipios = Municipio.objects.all()
		contexto = {'username': username,
                    'first_name': nombre,
                    'municipios': municipios,
                    'last_name': apellido,
                    'dui': dui,
                    'nit': nit,
                    'email': email,
                    'id_municipio': id_municipio,
                    'password1': password1,
                    'password2': password2,
              }

		if(username == "" or nombre == "" or apellido == "" or email == "" or id_municipio == "" or password1 == "" or password2 == ""):
			err = "Complete todos los campos por favor"
			contexto['err'] = err
			return render(request, 'auth/registro.html', contexto)

		if(password1 != password2):
			err = "Las contraseñas no coinciden"
			contexto['err'] = err
			return render(request, 'auth/registro.html', contexto)

		#validando que se nombre de usuario no exista en la BD
		if(User.objects.filter(username=username).exists()):
			err = "Ya Existe este usuario, ingrese otro por favor"
			contexto['err'] = err
			return render(request, 'auth/registro.html', contexto)
   
		if (Beneficiario.objects.exclude(DUI='').filter(DUI=dui).exists()):
			err="El DUI ingresado ya existe, por favor ingrese otro número de DUI"
			contexto['err']=err
			return render(request, 'auth/registro.html', contexto)

		if (Beneficiario.objects.exclude(NIT='').filter(NIT=nit).exists()):
				err="El NIT ingresado ya existe, por favor ingrese otro número de NIT"
				contexto['err']=err
				return render(request, 'auth/registro.html',contexto)

		if(User.objects.filter(email=email).exists()):
			err="El correo ingresado ha sido usado anteriormente, ingrese otro correo electrónico"
			contexto['err']=err
			return render(request, 'auth/registro.html', contexto)

		modelo_usuario = User()
		modelo_usuario.first_name = nombre
		modelo_usuario.last_name = apellido
		modelo_usuario.username = username
		modelo_usuario.email = email
		modelo_usuario.set_password(password1)
		modelo_usuario.save()

		modelo_beneficiario = Beneficiario()

		municipio_cod = Municipio.objects.get(id=id_municipio)
		modelo_beneficiario.codigo_municipio = municipio_cod

		modelo_beneficiario.codigo_usuario = modelo_usuario
		modelo_beneficiario.DUI = dui
		modelo_beneficiario.NIT = nit

		modelo_beneficiario.save()
		user = authenticate(request, username=username, password=password1)
		if user is not None:
			lg(request, user)
			return redirect('index')

	municipios = Municipio.objects.all()
	print(municipios)
	return render(request, 'auth/registro.html', {'municipios': municipios, 'err': err})
