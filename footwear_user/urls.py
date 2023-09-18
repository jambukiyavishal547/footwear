from django.urls import path
from .import views
urlpatterns = [

    ######################### Seller Side ################################
    
    path('seller-index/',views.seller_index,name='seller-index'),
    path('seller-change-password/',views.seller_change_password,name='seller-change-password'),
    path('seller-profile/',views.seller_profile,name='seller-profile'),
    path('seller-add-product/',views.seller_add_product,name='seller-add-product'),
    path('seller-view-product/',views.seller_view_product,name='seller-view-product'),
    path('seller-view-male/',views.seller_view_male,name='seller-view-male'),
    path('seller-view-female/',views.seller_view_female,name='seller-view-female'),
    path('seller-edit-product/<int:pk>/',views.seller_edit_product,name='seller-edit-product'),
    path('seller-delete-product/<int:pk>/',views.seller_delete_product,name="seller-delete-product"),
    path('seller-product-detail/<int:pk>/',views.seller_product_detail,name="seller-product-detail"),



    ######################### User Side ##################################


    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),

    path('add-to-cart/<int:pk>/',views.add_to_cart,name='add-to-cart'),
    path('cart/',views.cart,name='cart'),
    path('change-qty',views.change_qty,name='change-qty'),
    path('remove-from-cart/<int:pk>/',views.remove_from_cart,name='remove-from-cart'),

    path('add-to-wishlist/<int:pk>/',views.add_to_wishlist,name='add-to-wishlist'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('remove-from-wishlist/<int:pk>/',views.remove_from_wishlist,name='remove-from-wishlist'),

    path('women/',views.women,name='women'),
    path('product-detail/',views.product_detail,name='product-detail'),
    path('singel-product-detail/<int:pk>/',views.singel_product_detail,name='singel-product-detail'),

    path('create-checkout-session/',views.create_checkout_session,name='payment'),
    path('success.html/', views.success,name='success'),
    path('cancel.html/', views.cancel,name='cancel'),
    path('checkout/',views.checkout,name='checkout'),
    path('my-orders/',views.my_orders,name='my-orders'),
    
    path('men/',views.men,name='men'),
    path('order-complete/',views.order_complete,name='order-complete'),
    path('singup/',views.singup,name='singup'),
    path('singin/',views.singin,name='singin'),
    path('singout/',views.singout,name='singout'),
    path('profile/',views.profile,name='profile'),
    path('forgot-password/',views.forgot_password,name='forgot-password'),
    path('change-password/',views.change_password,name='change-password'),
    path('verify-otp/',views.verify_otp,name='verify-otp'),
    path('new-password/',views.new_password,name='new-password'),
]