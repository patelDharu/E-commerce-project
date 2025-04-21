from django.db import models

# Create your models here.
    
class category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to=None,height_field=None,width_field=None,max_length=100)  

    def __str__(self):
        return self.name
    

class catedata(models.Model):
   name = models.CharField(max_length=50)
   image = models.ImageField()

   def __str__(self):
        return self.name
    

class product(models.Model):
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='pro_img')
    category = models.ForeignKey(category,on_delete = models.CASCADE)

    def __str__(self):
       return self.name
    
class registration(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    mob = models.CharField(max_length=10)
    add = models.TextField()
    password = models.CharField(max_length=8)

    def __str__(self):
        return self.name    
    
class cart(models.Model):
    proid = models.ForeignKey(product,on_delete=models.CASCADE)
    userid = models.ForeignKey(registration,on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()
    totalprice = models.PositiveIntegerField()
    orderid = models.PositiveIntegerField(default='0')

    def __str__(self):
        return str(self.pk)
        
class order(models.Model):
    proid = models.ForeignKey(product,on_delete=models.CASCADE)
    userid = models.ForeignKey(registration,on_delete=models.CASCADE)
    add = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pin = models.CharField(max_length=6)
    # Grand_price = models.PositiveBigIntegerField()
    Total_price = models.PositiveBigIntegerField()
    payment_mode = models.CharField(max_length=20)
    transaction_id = models.CharField(max_length=100)
    datetime = models.DateTimeField(auto_now=True)
    mob = models.CharField(max_length=10,default='0')
    qty = models.PositiveIntegerField(default='0')
    orderid = models.TextField(default='cod',blank=True)

    def __str__(self):
        return str(self.pk)    
    