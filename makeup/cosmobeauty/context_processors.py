

from .models import Cart

def cart_data(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        total=0
        
        for c in cart:
            total+=int(c.product.price)*int(c.qty)
        if total>=1000:
            shipc=0
        else:
            shipc=100
        netamount=total+shipc
    else:
        cart = []
        total=0
        shipc=0
    return {'cart': cart,}
