"""
URL configuration for localstore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from tienda import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home.as_view(), name='home'),
    path('home/', views.Home.as_view(), name='home'),
    path('signup/', views.Signup.as_view(), name='signup'),
    path('index/', views.Index.as_view(), name='index'),
    path('index/<int:pedidoID>/', views.DetallePedido.as_view(), name='pedido_detalle'),
    path('index/eliminar/<int:pedidoID>/', views.EliminarPedido.as_view(), name='eliminar_pedido'),
    path('logout/', views.Signout.as_view(), name='logout'),
    path('signin/', views.Signin.as_view(), name='signin'),
    path('carrito/', views.CarritoView.as_view(), name='carrito'),
    path('carrito/agregar_al_carrito/<int:articulo_id>/', views.AgregarAlCarrito.as_view(), name='agregar_al_carrito'),
    path('carrito/actualizar_cantidad/<int:item_pk>/<int:cantidad>/', views.ActualizarCantidad.as_view(), name='actualizar_cantidad'),
    path('carrito/eliminar_del_carrito/<int:carrito_id>/', views.EliminarDelCarrito.as_view(), name='eliminar_del_carrito'),
    path('carrito/cancelar_carrito/', views.CancelarCarrito.as_view(), name='cancelar_carrito'),
    path('carrito/guardar_pedido/', views.GuardarPedido.as_view(), name='guardar_pedido'),
    path('pedido_detalle/<int:pedidoID>/', views.PedidoDetalle.as_view(), name='pedido_detalle'),
    path('marca/<int:marca_id>/', views.MarcaDetail.as_view(), name='marca_detail'),    
    path('productos/', views.Productos.as_view(), name='productos'),
    path('', include('tienda.urls')),
    path('api-token-auth/', views.generar_token),
    path('accounts/',include('allauth.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
