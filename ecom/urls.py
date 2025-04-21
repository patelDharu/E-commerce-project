from django.urls import path
# from .views import home
# from .views import cate
# from .views import categorydata
# from .views import index
# from .views import catpro
# from .views import productdetails
# from .views import register
# from .views import login

from .views import * 


urlpatterns = [
    path('home/',home,name='home'),
    path('category/',cate,name='category'),
    path('catedata/',categorydata,name='catedata'),
    path('',index,name='index'),
    path('catpro/<int:id>',catpro,name='catpro'),
    path('prodetails/<int:id>',productdetails,name='prodetails'),
    path('register/',register,name='register'),
    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),
    path('profile/',profile,name='profile'),
    path('cart/',cartview,name='cart'),
    path('additem/<int:id>',plusitem,name='additem'),
    path('delitem/<int:id>',minusitem,name='delitem'),
    path('delproduct/<int:id>',productremove,name='delproduct'),
    path('allproductremove/',allproductremove,name='allproductremove'),
    path('checkout/',checkout,name='checkout'),
    path('orderhistory/',orderhistory,name='orderhistory'),
    path('razorpay/',razorpayment,name='razorpayment'),
    path('paymenthandler/',paymenthandler,name='paymenthandler'),
    path('random_api_check/',random_api_check,name='random_api_check'),
    path('api_view_of_register/',api_view_of_register,name='api_view_of_register'),
    path('api_view_to_store',api_view_to_store,name='api_view_to_store')
]