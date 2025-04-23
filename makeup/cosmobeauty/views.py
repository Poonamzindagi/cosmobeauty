from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
import random as r
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import razorpay

from .models import *
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        category=Category.objects.filter(status='Active')
        product=Products.objects.filter(status='Active')[0:8]
        trending=Products.objects.filter(status='Active')
        cart=Cart.objects.filter(user=request.user)
        total=0
        shipc=0
        for c in cart:
            total+=int(c.product.price)*int(c.qty)
        if total>=1000 :
            shipc=0
        else:
            shipc=100

        netamount=total+shipc
        
    else:
        cart=[]
        category=Category.objects.filter(status='Active')
        product=Products.objects.filter(status='Active')
        trending=Products.objects.filter(status='Active')
        total=0
        shipc=0
        netamount=total+shipc
    return render(request,'index.html',{'category':category,'products':product,'trending':trending,'total':total,'shipc':shipc,'cart':cart,'net':netamount})

def userlogin(request):
    category=Category.objects.filter(status='Active')
    product=Products.objects.filter(status='Active')
    if request.method == 'POST':
        email=request.POST.get('email')
        password = request.POST.get('pwd1')
        u = authenticate(email=email, password=password)
        if u is not None:
            login(request, u)
            return redirect('mainpage')
        else:
            msg = "Invalid Username & Password"
            return render(request, 'index.html', {'msg':msg})
    return render(request,'index.html',{'category':category,'products':product})

def usersignup(request):
    if request.method=='POST' :
        email=request.POST.get('email')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        contact=request.POST.get('contact')
        pwd1=request.POST.get('pwd1')
        pwd2=request.POST.get('pwd2')
        if pwd1==pwd2:
            u=CustomUser.objects.create_user(email=email, first_name=first_name,last_name=last_name,password=pwd1,contact=contact)
        
            u.save()
        return redirect('userlogin')
      
    return render(request,'signup.html')



def productdetails(request,id):
    acategory=Category.objects.filter(status='Active')
    product=Products.objects.get(id=id)
    category=product.category
    showproduct=Products.objects.filter(status='Active',category=category)
    cart=Cart.objects.filter(user=request.user)
    total=0
    shipc=0
    
    for c in cart:
        total+=int(c.product.price)*int(c.qty)
    if total>=1000:
        shipc=0
    else:
        shipc=100

    netamount=total+shipc
    return render(request,'productdetails.html',{'product':product,'showproducts':showproduct,'total':total,'shipc':shipc,'net':netamount,'acategory':acategory})

def category(request,id):
    acategory=Category.objects.filter(status='Active')
    category=Category.objects.filter(status='Active')
    product=Products.objects.filter(category=id)
    showcategory=Category.objects.filter(id=id)
    cart=Cart.objects.filter(user=request.user)
    total=0
    shipc=0
    for c in cart:
        total+=int(c.product.price)*int(c.qty)
    if total>=1000:
        shipc=0
    else:
        shipc=100

    netamount=total+shipc
    return render(request, 'category.html',{'category':category,'acategory':acategory,'products':product,'showcategory':showcategory,'total':total,'shipc':shipc,'net':netamount})

def addtocart(request):
    if request.user.is_authenticated:
        u=request.user
        product=request.GET.get('product')
        pid=Products.objects.get(id=product)
        qty=request.GET.get('qty')
        cart,created=Cart.objects.get_or_create(product=pid,user=u)
        if not created:
            cart.qty+=int(qty)
            
            
        else:
            cart.qty=int(qty)
        cart.save()
        return HttpResponse('Add To Cart')
        
    else:
        return HttpResponse('Login')
    
def deletecart(request):
    id=request.GET.get('id')
    cart=Cart.objects.get(id=id)
    cart.delete()
    return HttpResponse('Item Deleted')

def updatecart(request):
    id=request.GET.get('id')
    nqty=request.GET.get('qty')
    cart=Cart.objects.get(id=id)
    cart.qty=nqty
    cart.save()
    return HttpResponse(' Updated ')

@login_required
def wishlisted(request):
    category=Category.objects.filter(status='Active')
    product=request.GET.get('product')
    if request.GET:
        u=request.user
        pid = Products.objects.get(id= product)
        like,created=Wishlist.objects.get_or_create(user=u,product = pid)
        if not created:
            like.delete()
            return HttpResponse('Remove from Wishlist')
        else:
            return HttpResponse('Add in Wishlist')
    wish = Wishlist.objects.filter(user=request.user)
    
    return render(request, 'wishlist.html',{'wish':wish,'category':category})

def deletewishlist(request):
    
    id=request.GET.get('id')
    wish=Wishlist.objects.filter(id=id)
    wish.delete()
    return HttpResponse('Item Deleted')   

def checkout(request):
    acategory=Category.objects.filter(status='Active')
    category=Category.objects.filter(status='Active')
    cart=Cart.objects.filter(user=request.user)
    uid=request.user
    orderid='ORD'+str(r.randint(1000,9999))
    total=0
    
    for c in cart:
        total+=int(c.product.price)*int(c.qty)
    if total>=1000:
        shipc=0
    else:
        shipc=100

    netamount=total+shipc
    if request.POST.get('placeorder'):
        for x in cart:
            order=Order.objects.create(user=uid, product=x.product ,qty=x.qty ,orderid=orderid ,status='Success')
            order.save()
            product=Products.objects.get(id=x.product.id)
            product.stock=int(product.stock)-int(x.qty)
            product.save()

        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        contact=request.POST.get('contact')
        add=request.POST.get('address')
        landmark=request.POST.get('landmark')
        address=add+","+ landmark
        city=request.POST.get('city')
        state=request.POST.get('state')
        
        zipcode=request.POST.get('zipcode')
        amount=request.POST.get('amount')
        payment_mode=request.POST.get('pay')
        
        order=Order.objects.filter(orderid=orderid).first()

        bill=Billing.objects.create(user=request.user, first_name=first_name, last_name=last_name,email=email, contact=contact, address=address ,city=city, state=state, zipcode=zipcode, amount=amount, payment_mode=payment_mode, orderid=order)

        bill.save()
        cart.delete()

        if payment_mode=='Online':
            return render(request,'payment.html',{'amount': int(request.POST.get('amount'))*100})
        else:
            return render(request,'completepayment.html')
        



    return render(request,'checkout.html',{'cart':cart,'total':total,'shipc':shipc,'net':netamount,'orderid':orderid,'category':category,'acategory':acategory})


@csrf_exempt
def complete_payment(request):
    if request.method == "POST":
        
        name = request.POST.get("name")
        amount = request.POST.get("amount")
        print("Amount received:", amount) 

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create(
            {"amount": float(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )
        
        return render(request,"completepayment.html", {'amount':int(amount)*100})




    
@login_required
def myorders(request):
    acategory=Category.objects.filter(status='Active')
    category=Category.objects.filter(status='Active')
    if request.user.is_authenticated:
        myorders=Order.objects.filter(user=request.user)
        cart=Cart.objects.filter(user=request.user)
        total=0
        shipc=0
        for c in cart:
            total+=int(c.product.price)*int(c.qty)
        if total>=1000:
            shipc=0
        else:
            shipc=100
        netamount=total+shipc
    else:
        myorders=[]
        cart=[]
        total=0
        shipc=0
    return render(request,'myorders.html',{'myorders':myorders,'category':category,'total':total,'shipc':shipc,'net':netamount,'acategory':acategory})

def searchitem(request):
    return render(request,'search.html')


def userlogout(request):
        logout(request)
        return redirect('mainpage')