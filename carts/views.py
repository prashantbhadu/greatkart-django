from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from store.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
# Create your views here.

def _cart_id(request):
    
    cart=request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart    



def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_variation = []

    # 🔹 Get selected variations
    if request.method == 'POST':
        for key in request.POST:
            value = request.POST.get(key)
            try:
                variation = Variation.objects.get(
                    product=product,
                    variation_category__iexact=key,
                    variation_value__iexact=value
                )
                product_variation.append(variation)
            except Variation.DoesNotExist:
                pass

    # 🔹 If user is logged in
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(
            product=product,
            user=request.user,
            is_active=True
        )

        if cart_items.exists():
            for item in cart_items:
                existing_variations = list(item.variations.all())
                if set(existing_variations) == set(product_variation):
                    item.quantity += 1
                    item.save()
                    return redirect('cart')

        # Create new cart item for user
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            user=request.user
        )

        if product_variation:
            cart_item.variations.add(*product_variation)

        cart_item.save()

    # 🔹 If user is NOT logged in (Guest user)
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))

        cart_items = CartItem.objects.filter(
            product=product,
            cart=cart,
            is_active=True
        )

        if cart_items.exists():
            for item in cart_items:
                existing_variations = list(item.variations.all())
                if set(existing_variations) == set(product_variation):
                    item.quantity += 1
                    item.save()
                    return redirect('cart')

        # Create new cart item for guest
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )

        if product_variation:
            cart_item.variations.add(*product_variation)

        cart_item.save()

    return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        cart_item.delete()
    except:
        pass
    return redirect('cart')

def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0

        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(
                user=request.user,
                is_active=True
            )
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(
                cart=cart,
                is_active=True
            )

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (2 * total) / 100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'store/cart.html', context)

    
@login_required(login_url='login')
def checkout(request,total=0,quantity=0,cart_items=None):
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:    
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total+=(cart_item.product.price*cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2*total)/100 
        grand_total = total + tax   
    except ObjectDoesNotExist:
        pass #just ignore  

    context = {
        'total': total, 
        'quantity': quantity,
        'cart_items': cart_items,
        'tax':tax,
        'grand_total': grand_total,
    }      
    return render(request,'store/checkout.html', context)
