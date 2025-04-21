from django.contrib import admin
# from .models import blog
# from .models import author
# from .models import category
# from .models import catedata
# from .models import product
# from .models import registration

from .models import *
# Register your models here.

class category_(admin.ModelAdmin):
    list_display = ['id','name','image']

admin.site.register(category,category_)  
   

class catedata_(admin.ModelAdmin):
    list_display=['id','name','image']

admin.site.register(catedata,catedata_)    

class pro_admin(admin.ModelAdmin):
    list_display = ['id','name','stock','price','description','category']

admin.site.register(product,pro_admin)   

class reg_admin(admin.ModelAdmin):
    list_display = ['id','name','email','mob','add']

admin.site.register(registration,reg_admin)

class cart_admin(admin.ModelAdmin):
    list_display = ['id','proid','userid','qty','totalprice','orderid']

admin.site.register(cart,cart_admin)

class order_admin(admin.ModelAdmin):
    list_display = ['id','proid','userid','Total_price','payment_mode','transaction_id','datetime','qty','orderid']

admin.site.register(order,order_admin)    