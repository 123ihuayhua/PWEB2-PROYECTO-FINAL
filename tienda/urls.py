from rest_framework import routers
from .api import *

router = routers.DefaultRouter()
    
router.register('api/vendedor', VendedorViewSet, 'vendedor')
router.register('api/cliente', ClienteViewSet, 'cliente')
router.register('api/pedido', PedidoViewSet, 'pedido')
router.register('api/marca', MarcaViewSet, 'tienda')
router.register('api/tipoArt', TipoArticuloViewSet, 'tienda')
router.register('api/carrito', CarritoViewSet, 'Carrito')
router.register('api/articulo', ArticuloViewSet, 'articulo')

urlpatterns = router.urls 
