from django.contrib import admin
from .models import *
#Mostrar detalles en Vendedor 
class VendedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'dni')

    def nombre(self, obj): 
        return obj.VenNom
    nombre.short_description = 'Nombre'

    def apellido(self, obj): 
        return obj.VenApePat
    apellido.short_description = 'Apellido'

    def dni(self, obj): 
        return obj.VenDNI
    dni.short_description = 'DNI'

#Mostrar detalles en Cliente
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'dni')

    def nombre(self, obj): 
        return obj.CliNom
    nombre.short_description = 'Nombre'

    def apellido(self, obj): 
        return obj.CliApePat
    apellido.short_description = 'Apellido'

    def dni(self, obj): 
        return obj.CliDNI
    dni.short_description = 'DNI'

#Mostrar detalles en Artículo
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ('nombre_articulo', 'marca', 'stock', 'precio_unitario')

    def nombre_articulo(self, obj):
        return obj.ArtNom
    nombre_articulo.short_description = 'Nombre'

    def marca(self, obj):
        return obj.ArtMarCod
    marca.short_description = 'Marca'

    def stock(self, obj):
        return obj.ArtSto
    stock.short_description = 'Cantidad en Stock'

    def precio_unitario(self, obj):
        return f'S/ {obj.ArtPreUni:,.2f}'
    precio_unitario.short_description = 'Precio Unitario'


#Vistas y modelos
admin.site.register(Vendedor, VendedorAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Marca)
admin.site.register(TipoArticulo)
admin.site.register(Articulo, ArticuloAdmin)
admin.site.register(Pedido)
admin.site.register(Carrito)