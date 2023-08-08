from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import PedidoForm, RegistroForm
from .models import Carrito, Pedido, Cliente, Marca, Articulo
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.generic import View
from django.utils.decorators import method_decorator


# Vista principal

class Home(View):
    def get(self, request, *args, **kwargs):
        marcas = Marca.objects.all()
        arts = Articulo.objects.all()
        context = {'marcas': marcas, 'arts': arts}
        return render(request, 'home.html', context)

# Registrarse (usuario)
class Signup(View):
    def get(self, request, *args, **kwargs):
        form = RegistroForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request, *args, **kwargs):
        print(request.POST)
        form = RegistroForm(request.POST)
        if form.is_valid():
            if request.POST['password1'] == request.POST['password2']:
                try:
                    # Crear usuario
                    user = Cliente.objects.create_user(
                        username=request.POST['username'],
                        password=request.POST['password1'],
                        CliDNI=request.POST['CliDNI'],
                        CliApePat=request.POST['CliApePat'],
                        CliNom=request.POST['CliNom'],
                        CliEstReg=True
                    )
                    login(request, user)
                    return redirect('home')
                except IntegrityError:
                    return render(request, 'signup.html', {
                    'form': RegistroForm,
                    'error': 'El usuario ya existe'
                })
        print(form.errors)
        return render(request, 'signup.html', {
            'form': form,
        })

# Logearse
class Signin(View):
    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
        return render(request, 'signin.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                request, username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                print("usuario correcto")
                return redirect('home')
        return render(request, 'signin.html', {'form': form, 'error': 'Usuario o contraseña incorrecta'})

# Salir de la sesión
class Signout(View):
    def get(self, request):
        logout(request)
        return redirect('home')

# Ver pedidos
@method_decorator(login_required, name='dispatch')
class Index(View):
    def get(self, request, *args, **kwargs):
        pedido = Pedido.objects.filter(PedCabCodCli=request.user)
        return render(request, 'index.html', {'pedidos': pedido})

# Detalle pedido
@method_decorator(login_required, name='dispatch')
class DetallePedido(View):
    def get(self, request, pedidoID, *args, **kwargs):
        pedido_cabecera = get_object_or_404(
            Pedido, pk=pedidoID, PedCabCodCli=request.user)
        detalles_pedido = Pedido.objects.filter(PedDetCodCab=pedido_cabecera)

        if detalles_pedido.exists():
            detalle = detalles_pedido.first()
        else:
            detalle = Pedido(PedDetCodCab=pedido_cabecera)

        form = PedidoForm(instance=detalle)
        carrito = request.session.get('carrito', {})
        articulos = Articulo.objects.filter(pk__in=carrito.keys())
        detalles = []
        for carrito in pedido_cabecera.PedDetArtCod.all():
            detalles.append({
                'articulo': carrito.articulo,
                'cantidad': carrito.cantidad,
                'subtotal': carrito.subtotal,
                'precio_uni': carrito.articulo.ArtPreUni, 
            })
            print("Se ha registrado productos")
        return render(request, 'pedido_detalle.html', {
            'pedido_cabecera': pedido_cabecera,
            'detalle': detalle,
            'form': form,
            'detalles': detalles
        })

    def post(self, request, pedidoID, *args, **kwargs):
        pedido_cabecera = get_object_or_404(
            Pedido, pk=pedidoID, PedCabCodCli=request.user)
        detalles_pedido = Pedido.objects.filter(PedDetCodCab=pedido_cabecera)

        if detalles_pedido.exists():
            detalle = detalles_pedido.first()
        else:
            detalle = Pedido(PedDetCodCab=pedido_cabecera)

        form = PedidoForm(request.POST, instance=detalle)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})

# Elimininar pedido
@method_decorator(login_required, name='dispatch')
class EliminarPedido(View):
    def get(self, request, pedidoID, *args, **kwargs):
        pedido_cabecera = get_object_or_404(
            Pedido, pk=pedidoID, PedCabCodCli=request.user)
        detalles_pedido = Pedido.objects.filter(pk=pedidoID)

        for carrito in pedido_cabecera.PedDetArtCod.all():
            carrito.setstatus(True)
        pedido_cabecera.PedDetEstReg = False
        pedido_cabecera.save()
        return redirect('index')

# Marcas
class MarcaDetail(View):
    def get(self, request, marca_id, *args, **kwargs):
        marca = get_object_or_404(Marca, pk=marca_id)
        arts = Articulo.objects.filter(ArtMarCod=marca)
        context = {'marca': marca, 'arts': arts}
        return render(request, 'marca_msi.html', context)

# Carrito de compras
@method_decorator(login_required, name='dispatch')
class CarritoView(View):
    def get(self, request, *args, **kwargs):
        carrito = Carrito.objects.filter(usuario=request.user, status = True)
        total = sum(item.subtotal for item in carrito)
        return render(request, 'carrito.html', {'carrito': carrito, 'total': total})

# Agregar al carrito
@method_decorator(login_required, name='dispatch')
class AgregarAlCarrito(View):
    def post(self, request, articulo_id, *args, **kwargs):
        articulo = get_object_or_404(Articulo, pk=articulo_id)
        carrito, created = Carrito.objects.get_or_create(
            usuario=request.user, articulo=articulo)
        if not created:
            carrito.cantidad += 1
            carrito.save()
        return redirect('carrito')

# Eliminar Producto
@method_decorator(login_required, name='dispatch')
class EliminarDelCarrito(View):
    def post(self, request, carrito_id, *args, **kwargs):
        carrito = get_object_or_404(
            Carrito, pk=carrito_id, usuario=request.user)
        carrito.delete()
        return redirect('carrito')

# Carrito cantidad actualizar
class ActualizarCantidad(View):
    def post(self, request, item_pk, cantidad, *args, **kwargs):
        try:
            carrito_item = get_object_or_404(Carrito, pk=item_pk)
            carrito_item.cantidad = cantidad
            carrito_item.save()
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'status': 'not ok', 'message': str(e)})
            
# Cancelar carrito
class CancelarCarrito(View):
    def post(self, request, *args, **kwargs):
        carrito = Carrito.objects.filter(usuario=request.user, status = True)
        carrito.delete()
        return redirect('carrito')

#Guardar pedido
@method_decorator(login_required, name='dispatch')
class GuardarPedido(View):
    def get(self, request, *args, **kwargs):
        # messages.warning(request, 'No se permiten solicitudes GET.')
        return redirect('index')

    def post(self, request, *args, **kwargs):
        carrito = Carrito.objects.filter(usuario=request.user)
        if carrito.exists():
            pedido_cabecera = Pedido(PedCabCodCli=request.user)
            pedido_cabecera.save()
            for item in carrito:
                articulo = item.articulo
                cantidad = item.cantidad
                cantidad * articulo.ArtPreUni
                carrito_item = Carrito(usuario=request.user, articulo=articulo, cantidad=cantidad)
                carrito_item.save()
                pedido_cabecera.PedDetArtCod.add(carrito_item)  
                item.setstatus(False)
                item.save()
            pedido_cabecera.save()
            carrito.delete()
            return redirect('pedido_detalle', pedidoID=pedido_cabecera.pk)
        else:
            messages.warning(request, 'No hay artículos en el carrito.')
            return redirect('index')

# Pedido detalle
@method_decorator(login_required, name='dispatch')
class PedidoDetalle(View):
    def get(self, request, pedidoID, *args, **kwargs):
        pedido = get_object_or_404(
            Pedido, pk=pedidoID, PedCabCodCli=request.user)
        detalles = []
        for carrito in Carrito.objects.filter(usuario=request.user, pedido=pedido):
            detalles.append({
                'articulo': carrito.articulo,
                'cantidad': carrito.cantidad,
                'precio_uni': carrito.articulo.ArtPreUni,
                'subtotal': carrito.subtotal,
            })
        return render(request, 'pedido_detalle.html', {'pedido': pedido, 'detalles': detalles})

# Productos
class Productos(View):
    def get(self, request, *args, **kwargs):
        marcas = Marca.objects.all()
        arts = Articulo.objects.all()
        context = {'marcas': marcas, 'arts': arts}
        return render(request, 'productos.html', context)

# Token
@api_view(['POST'])
def generar_token(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        token = user.generate_auth_token()
        return Response({'token': token})
    else:
        return Response({'error': 'Credenciales inválidas'})
