from django.shortcuts import render
from .models import Galeria, Insumo ,Slider , MisionVision, Contacto
# IMPORTAR LA TABLA DE USUARIOS DEL admin de Django
from django.contrib.auth.models import User

# importar las librerias de authentication (autentificar), logout(salir), login(acceder)
from django.contrib.auth import authenticate, logout, login as login_autent

# agregar un decorador que evite el ingreso a unas paginas (requiere estar logeado) permission_required (debe tener un permiso)
from django.contrib.auth.decorators import login_required, permission_required

# importar peticiones HTTP
import requests

# ------------------------------------------------------------------------------------
# incorporar las librerias necesarias para trabajar con la carga de adtos
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse, HttpResponseBadRequest
from django.core import serializers
import json
from fcm_django.models import FCMDevice
# creacion de la vista para el desarrollo del metodo

@csrf_exempt
@require_http_methods(['POST'])
def guardar_token(request):
    body = request.body.decode('utf-8')
    datos_body = json.loads(body)
    token = datos_body['token']
    # preguntar si el token existe
    existe = FCMDevice.objects.filter(registration_id=token,active=True)
    if len(existe)>0:
        return HttpResponseBadRequest(json.dumps({'mensaje','el token existe'}))
    dispositivo = FCMDevice()
    dispositivo.registration_id = token
    dispositivo.active = True
    # solo si el usuario esta registrado antes
    if request.user.is_authenticated:
        dispositivo.user = request.user
    # grabar el dipositivo
    try:
        dispositivo.save()
        return HttpResponse(json.dumps({'mensaje','dispositivo almacenado'}))
    except:
        return HttpResponseBadRequest(json.dumps({'mensaje','no pudo almacenar el token'}))
# ------------------------------------------------------------------------------------


# Create your views here.
def logout_vista(request):
    logout(request)
    slider = Slider.objects.all()
    return render(request,'web/index.html',{'imagSlider':slider})

def login(request):
    slider = Slider.objects.all()
    if request.POST:
        usuario = request.POST.get("NombreUsuario")
        password = request.POST.get("Pass")
        us = authenticate(request,username=usuario,password=password)
        if us is not None and us.is_active:
            login_autent(request,us)
            return render(request,'web/index.html',{'imagSlider':slider},{'user':us})
        else:
            return render(request,'web/login.html', {'msg':'El usuario NO existe'}) 
    return render(request, 'web/login.html')

## FORMULARIO REGISTRO
def formulario(request):
    slider = Slider.objects.all()
    if request.POST:
        nombre = request.POST.get("Nombre")
        apellido = request.POST.get("Apellido")
        correo = request.POST.get("Email")
        usuario = request.POST.get("NombreUsuario")
        pass1 = request.POST.get("Pass1")
        pass2 = request.POST.get("Pass2")

        try: #Si existe el usuario
            u = User.objects.get(username=usuario)
            mensaje = "El nombre de Usuario ya existe"
            return render(request,'web/reg-formulario.html',{'msg':mensaje})

        except: #Si NO existe el usuario
            try: 
                #Si existe el correo
                u = User.objects.get(email=correo)
                mensaje = "El correo ya posee un usuario asociado."
                return render(request,'web/reg-formulario.html',{'msg':mensaje})
            except:
                #No existe el usuario
                if pass1 != pass2: #Pregunta si las contraseñas no son iguales
                    mensaje = "Las contraseñas no coinciden"
                    return render(request,'web/reg-formulario.html',{'msg':mensaje})

                u = User()
                u.first_name = nombre
                u.last_name = apellido
                u.email = correo
                u.username = usuario
                u.set_password(pass1)
                u.save()
                us = authenticate(request,username=usuario,password=pass1)
                login_autent(request,us)
                return render(request,'web/index.html',{'imagSlider':slider},{'user':us})
    return render(request,'web/reg-formulario.html')

# FORMULARIO PARA ADMINISTRAR LOS INSUMOS    
@login_required(login_url='/login/') #pide que este logeado
@permission_required('StarWash.view_insumo', login_url='/login/') #pide un permiso para ver insumos
def adminInsumo(request):
    #lista_insumos = Insumo.objects.all()
    # Se recupera todos los insumos en formato json
    response = requests.get("http://127.0.0.1:8000/api/insumos/")
    lista_insumos = response.json()
    #Si envia el metodo POST
    if request.POST:
        accion = request.POST.get("accion")
        #Pregunta que accion es con el Value
        if accion == "Modificar":
            nombreIns = request.POST.get("NombreInsumo")
            precioIns = request.POST.get("Precio")
            descIns = request.POST.get("Descripcion")
            stockIns = request.POST.get("Stock")
            try:
                ins = Insumo.objects.get(nombre=nombreIns)
                ins.precio = precioIns
                ins.descripcion = descIns
                ins.stock = stockIns
                ins.save()
                mensaje = "Insumo Modificado correctamente"
            except:
                mensaje = "NO modifico el insumo"
            lista_insumos = Insumo.objects.all()
            return render(request,'web/admin_insumos.html',{'lista_insumos':lista_insumos,'mensaje':mensaje})

        if accion == "Eliminar":
            try:
                nombreInsumo = request.POST.get("NombreInsumo")
                ins = Insumo.objects.get(nombre=nombreInsumo)
                ins.delete()
                mensaje = "Insumo Eliminado correctamente"
            except:
                mensaje = "NO elimino Insumo"
            lista_insumos = Insumo.objects.all()
            return render(request,'web/admin_insumos.html',{'lista_insumos':lista_insumos,'mensaje':mensaje})

        if accion == "Crear":
            nombreIns = request.POST.get("NombreInsumo")
            precioIns = request.POST.get("Precio")
            descIns = request.POST.get("Descripcion")
            stockIns = request.POST.get("Stock")
            
            ins = Insumo(
                nombre = nombreIns,
                precio = precioIns,
                descripcion = descIns,
                stock = stockIns
            )

            ins.save()
            mensaje = "Insumo Creado correctamente"
            return render(request,'web/admin_insumos.html',{'lista_insumos':lista_insumos,'mensaje':mensaje})

    return render(request,'web/admin_insumos.html',{'lista_insumos':lista_insumos})

### AGREGAR INSUMOS   
@login_required(login_url='/login/') #pide que este logeado
@permission_required('StarWash.add_insumo', login_url='/login/') #pide un permiso de agregar insumos
def insumos(request):
    if request.POST:
        nombreIns = request.POST.get("NombreInsumo")
        precioIns = request.POST.get("Precio")
        descIns = request.POST.get("Descripcion")
        stockIns = request.POST.get("Stock")
        
        '''ins = Insumo(
            nombre = nombreIns,
            precio = precioIns,
            descripcion = descIns,
            stock = stockIns
        )
        ins.save()'''

        # GUARDAR UTILIZANDO LA API
        datos_insumo = {
            "nombre" : nombreIns,
            "precio" : precioIns,
            "descripcion" : descIns,
            "stock" : stockIns
        }
        requests.post("http://127.0.0.1:8000/api/insumos/", data=datos_insumo)
        # envio el token
        dispositivos = FCMDevice.objects.filter(active=True)
        dispositivos.send_message(
            title='Nuevo Insumo Agregado',
            body='Tenemos un nuevo insumo: ' + nombreIns,
            icon='/static/img/logo/Logo.png'
        )
        return render(request,'web/reg-insumo.html', {'mensaje':'Se registro el Insumo'})
    return render(request,'web/reg-insumo.html')

### ELIMINA EL INSUMO
@login_required(login_url='/login/') #pide que este logeado
@permission_required('StarWash.view_insumo', login_url='/login/') #pide un permiso para ver insumos
@permission_required('StarWash.delete_insumo', login_url='/login/') #pide un permiso para ver insumos
def eliminar_insumo(request, id):
    #lista_insumos = Insumo.objects.all()
    # Se recupera todos los insumos en formato json
    response = requests.get("http://127.0.0.1:8000/api/insumos/")
    lista_insumos = response.json()
    try:
        ins = Insumo.objects.get(nombre=id)
        ins.delete()
        mensaje = "Insumo Eliminado"
    except:
        mensaje = "NO Elimino Insumo"
    return render(request,'web/admin_insumos.html',{'mensaje':mensaje,'lista_insumos':lista_insumos})
        
### BUSCA EL INSUMO
@login_required(login_url='/login/') #pide que este logeado
@permission_required('StarWash.view_insumo', login_url='/login/') #pide un permiso para ver insumos
def buscar(request,id):
    try:
        insumo = Insumo.objects.get(nombre=id)
        return render(request,'web/formulario_insumo_mod.html',{'insumo':insumo})
    except :
        msg = 'No existe el Insumo'
    #lista_insumos = Insumo.objects.all()
    # Se recupera todos los insumos en formato json
    response = requests.get("http://127.0.0.1:8000/api/insumos/")
    lista_insumos = response.json()
    return render(request,'web/admin_insumos.html',{'lista_insumos':lista_insumos,'mensaje':msg})

### MODIFICAR EL INSUMO
@login_required(login_url='/login/') #pide que este logeado
@permission_required('StarWash.view_insumo', login_url='/login/') #pide un permiso para ver insumos
@permission_required('StarWash.change_insumo', login_url='/login/') #pide un permiso para ver insumos
def modificar(request):
    if request.POST:
        nombreIns = request.POST.get("NombreInsumo")
        precioIns = request.POST.get("Precio")
        descIns = request.POST.get("Descripcion")
        stockIns = request.POST.get("Stock")
        
        try:
            i = Insumo.objects.get(nombre=nombreIns)
            i.precio = precioIns
            i.descripcion = descIns
            i.stock = stockIns
            i.save()
            msg = 'Se modifico el Insumo'
        except:
            msg = 'No se modifico'
    #lista_insumos = Insumo.objects.all()
    # Se recupera todos los insumos en formato json
    response = requests.get("http://127.0.0.1:8000/api/insumos/")
    lista_insumos = response.json()
    return render(request,'web/admin_insumos.html',{'lista_insumos':lista_insumos,'mensaje':msg})

def index(request):
    slider = Slider.objects.all()
    return render(request,'web/index.html',{'imagSlider':slider})

def conocenos(request):
    myv = MisionVision.objects.all()
    return render(request,'web/conocenos.html',{'myv':myv})

def ubicacion(request):
    return render(request,'web/ubicacion.html')

def galeria(request):
    gal = Galeria.objects.all()
    return render(request,'web/galeria.html',{'imagenes_galeria':gal})

def contacto(request):
    if request.POST:
        nombreCont = request.POST.get("Nombre")
        apellidoCont = request.POST.get("Apellido")
        asuntoCont = request.POST.get("Asunto")
        tipoCont = request.POST.get("TipoContacto")
        mensajeCont = request.POST.get("Mensaje")

        cont = Contacto()
        cont.nombre=nombreCont
        cont.apellido=apellidoCont
        cont.asunto=asuntoCont
        cont.tipo=tipoCont
        cont.mensaje=mensajeCont
        cont.save()

        # envio el token
        dispositivos = FCMDevice.objects.filter(active=True)
        dispositivos.send_message(
            title='Nuevo Solicitud De Contacto',
            body='Tipo de Solicitud: '+tipoCont,
            icon='/static/img/logo/Logo.png'
        )
        return render(request,'web/contacto.html',{'msg':'Se ha enviado su formulario.'})    
    return render(request,'web/contacto.html')


 