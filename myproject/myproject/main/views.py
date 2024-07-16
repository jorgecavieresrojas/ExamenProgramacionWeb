# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Carrito, CarritoItem
from .forms import AddToCartForm
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static


def index(request):
    productos = Producto.objects.all()
    return render(request, 'main/index.html', {'productos': productos})

@login_required
def add_to_cart(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            cantidad = form.cleaned_data['cantidad']
            carrito_item, created = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto)
            if not created:
                carrito_item.cantidad += cantidad
            else:
                carrito_item.cantidad = cantidad
            carrito_item.save()
            return redirect('view_cart')
    else:
        form = AddToCartForm()
    
    return render(request, 'main/add_to_cart.html', {'producto': producto, 'form': form})

@login_required
def view_cart(request):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    return render(request, 'main/view_cart.html', {'carrito': carrito})

@login_required
def checkout(request):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    if request.method == 'POST':
        carrito.items.clear()  # Vacia el carrito después de la compra
        return redirect('index')
    return render(request, 'main/checkout.html', {'carrito': carrito})
