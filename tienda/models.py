from django.db import models
from django.contrib.auth.models import User, AbstractUser
from rest_framework.authtoken.models import Token
# Create your models here.

# Vendedor
class Vendedor(models.Model):
    VenDNI = models.CharField(max_length=8, unique=True)
    VenApePat = models.CharField(max_length=20)
    VenNom = models.CharField(max_length=20)
    VenEstReg = models.BooleanField(default=True)
    # Mostrar nombre del vendedor

    def __str__(self):
        nombre = self.VenNom + ' ' + self.VenApePat
        return nombre

# Cliente
class Cliente(AbstractUser):
    CliDNI = models.CharField(max_length=8)
    CliApePat = models.CharField(max_length=20)
    CliNom = models.CharField(max_length=20)
    CliEstReg = models.BooleanField(default=True)

    # Mostrar nombre completo del cliente
    def __str__(self):
        return self.CliNom + ' ' + self.CliApePat

    password = models.CharField(max_length=128, null=True)
    username = models.CharField(max_length=150, unique=True, null=True)

    def generate_auth_token(self):
        token, created = Token.objects.get_or_create(user=self)
        return token.key

# Marca
class Marca(models.Model):
    MarNom = models.CharField(max_length=20)
    MarImg = models.ImageField(upload_to='imagenes/imgs', null=True)
    MarEstReg = models.BooleanField(default=True)
    # Mostrar nombre de las marcas

    def __str__(self):
        return self.MarNom

# Tipo Artículo


class TipoArticulo(models.Model):
    TipArtNom = models.CharField(max_length=20)
    TipArtEstReg = models.BooleanField(default=True)
    # Mostrar nombre de los tipos de artículos

    def __str__(self):
        return self.TipArtNom

# Articulo
class Articulo(models.Model):
    ArtMarCod = models.ForeignKey(Marca, on_delete=models.CASCADE, null=True)
    ArtTipCod = models.ForeignKey(
        TipoArticulo, on_delete=models.CASCADE, null=True)
    ArtNom = models.CharField(max_length=50, null=True)
    ArtDes = models.TextField(
        max_length=1000, help_text='Ingresa la descripción del artículo', null=True)
    ArtImg = models.ImageField(upload_to='imagenes/imgs', null=True)
    ArtSto = models.PositiveSmallIntegerField()
    ArtPreUni = models.FloatField()
    ArtEstReg = models.BooleanField(default=True)
    # Mostrar nombre del Artículo

    def __str__(self):
        return self.ArtNom

    def disminuir_stock(self, cantidad):
        self.ArtSto -= cantidad
        self.save()

    def aumentar_stock(self, cantidad):
        self.ArtSto += cantidad
        self.save()

# Carrito de Compras
class Carrito(models.Model):
    usuario = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    status = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.usuario} - {self.articulo}"

    def save(self, *args, **kwargs):
        if self.cantidad > self.articulo.ArtSto:
            raise Exception(f'La cantidad de "{self.articulo.ArtNom}" en el carrito supera el stock disponible.')
        return super().save(*args, **kwargs)
    
    def setstatus(self, value):
        if self.status != value:
            if self.status:
                self.articulo.ArtSto -= self.cantidad
                self.articulo.save()
            
            else: 
                self.articulo.ArtSto += self.cantidad
                self.articulo.save()
        self.status = value
        
    @property
    def subtotal(self):
        return self.cantidad * self.articulo.ArtPreUni

    def total(self):
        return self.subtotal()

# Pedido
class Pedido(models.Model):  # Cambiar modelo manytomany
    PedCabCodCli = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    PedCabFec = models.DateField(auto_now_add=True)
    PedDetArtCod = models.ManyToManyField(Carrito, symmetrical=False)
    PedDetEstReg = models.BooleanField(default=True)
    _total = 0

    @property
    def total(self):
        # Calculo total
        self._total = 0
        for c in self.PedDetArtCod.all():
            self._total += c.subtotal
        return self._total

    def __str__(self):
        return f"{self.PedCabCodCli} - {self.PedCabFec}"

# class PedidoDetalle(models.Model):
#     pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
#     carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.pedido} - {self.carrito}"

#     @property
#     def subtotal(self):
#         return self.carrito.subtotal