
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='mainpage'),
    path('userlogin',views.userlogin,name='userlogin'),
    path('usersignup', views.usersignup),
    path('product/<int:id>',views.productdetails),
    path('categories/<int:id>',views.category),
    path('addtocart',views.addtocart),
    path('deletefromcart',views.deletecart),
    path('updatecart',views.updatecart),
    path('wishlist',views.wishlisted),
    path('delwishlist',views.deletewishlist),
    path('checkout',views.checkout),
    path('complete_payment',views.complete_payment),
    path('myorders',views.myorders),
    path('search',views.searchitem),
    path('userlogout',views.userlogout)
]