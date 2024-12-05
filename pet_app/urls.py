from django.urls import path
from . import views
from .views import *
urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.logout, name='logout'),
    path('view_pets_products/<int:category_id>/',views.view_pets_products,name="view_pets_products"),

# ////////////////////////// ADMIN ////////////////////////////////////////
    path('adm_home', views.adm_home, name='adm_home'),
    path('login_page', views.login_page, name='login_page'),
    path('manage_users', views.manage_users, name='manage_users'),
    path('manage_sellers', views.manage_sellers, name='manage_sellers'),
    path('manage_shop', views.manage_shop, name='manage_shop'),
    path('manage_expert', views.manage_expert, name='manage_expert'),
    path('delete_user/<int:pk>/', views.delete_user, name='delete_user'),
    path('view_pets_category',views.view_pets_category,name='view_pets_category'),
    path('add_category',views.add_category,name='add_category'),
    path('delete_category/<int:pk>/', views.delete_category, name='delete_category'),

# //////////////////////////// SHOP //////////////////////////////////////////////
    
    path('shop_register', views.shop_register, name="shop_register"),
    path('shop_home',views.shop_home,name='shop_home'),
    path('add_product',views.add_product,name='add_product'),
    path('view_pets',views.view_pets,name='view_pets'),
    path('view_products',views.view_products,name='view_products'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('view_product_order',views.view_product_order,name='view_product_order'),
    path('delete_order/<int:order_id>',views.delete_order,name='delete_order'),
    path('deliver_order/<int:order_id>',views.deliver_order,name='deliver_order'),
    path('search1',views.search1,name="search1"),
    
# ///////////////////////////    //////////////////////////////////////////////////





    path('search',views.search,name="search"),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<str:item_type>/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/increment/<int:item_id>/', views.increment_cart_item, name='increment_cart_item'),
    path('cart/decrement/<int:item_id>/', views.decrement_cart_item, name='decrement_cart_item'),
    path('cart/checkout/', views.checkout_view, name='checkout_view'),    
    path('pet_booking/<int:pet_id>', views.pet_booking, name='pet_booking'),
    path('booking/', views.booking, name='booking'),
    path('manage_booking', views.manage_booking, name="manage_booking"),
    path('cancel_booking/<int:booking_id>', views.cancel_booking, name="cancel_booking"),
    path('deliveryboy_home/', views.deliveryboy_home, name="deliveryboy_home"),
    path('view_order/', views.view_order, name="view_order"),
    path('update_delivery/<int:assign_id>/', views.update_delivery, name="update_delivery"),
    path('update_order_status/', views.update_order_status, name="update_order_status"),
    path('assign_booking/<int:booking_id>/', views.assign_booking, name="assign_booking"),
    path('assign_delivery/', views.assign_delivery, name="assign_delivery"),
    path('generate_account_details/', views.generate_account_details, name="generate_account_details"),
    path('payment_page/', views.payment_page, name="payment_page"),
    path('payment/', views.payment, name="payment"),
    path('view_account/', views.view_account, name="view_account"),
    path('view_payments/', views.view_payments, name="view_payments"),
    path('view_bookings/', views.view_bookings, name="view_bookings"),





    

]

