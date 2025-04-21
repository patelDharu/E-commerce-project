from django.shortcuts import render , HttpResponse , redirect
# from .models import category
# from .models import catedata
# from .models import product
# from .models import registration

from .models import *


# Create your views here.

def home(request):
    return HttpResponse("This is my first view functions......")


def cate(request): 
    categorydata =category.objects.all()
    return render(request,'category.html',{'categorydata':categorydata})


def categorydata(request):
    obj = catedata()
    if request.method == 'POST' and request.FILES:
        obj.name = request.POST['name']
        obj.image = request.FILES['image']
        obj.save()
    return render(request,'catedata.html')

def index(request):
    if 'email' in request.session:
        loggedin_user = registration.objects.get(email = request.session['email'])
        catdata=category.objects.all()
        return render(request,'index.html',{'catdata':catdata,'loggedin':loggedin_user})
    else:
        catdata = category.objects.all()
        return render(request,'index.html',{'catdata':catdata})
 

def catpro(request,id):
    if 'email' in request.session:
        loggedin_user = registration.objects.get(email=request.session['email'])
        productdata = product.objects.filter(category = id)
        return render(request,'catpro.html',{'prodata':productdata,'loggedin':loggedin_user})
    else:
        productdata = product.objects.filter(category = id)
        return render(request,'catpro.html',{'prodata':productdata})

def productdetails(request,id):
    singleproductdetails = product.objects.get(id = id)
    if request.method == 'POST':
        if 'email' in request.session:
            loggedinuser = registration.objects.get(email = request.session['email'])    
            addtocart = cart()
            addtocart.proid = singleproductdetails
            addtocart.userid = loggedinuser
            addtocart.qty =request.POST['qty']
            addtocart.totalprice = int(addtocart.qty) * int(singleproductdetails.price)
            if singleproductdetails.stock <=0:
                return render(request,'product.html',{'prodetails':singleproductdetails,'loggedin':loggedinuser,'out_of_stock':'unavailable stock...!'})
            else:
                if int(request.POST['qty']) > singleproductdetails.stock:
                    return render(request,'product.html',{'prodetails':singleproductdetails,'loggedin':loggedinuser,'extra':'minus your product...!'})
                else:
                    already_in_cart = cart.objects.filter(proid = singleproductdetails,userid= loggedinuser,orderid = '0')
                    if already_in_cart: 
                        already_in_cart = cart.objects.get(proid = singleproductdetails,userid= loggedinuser,orderid = '0')
                        already_in_cart.qty = already_in_cart.qty + int(addtocart.qty)
                        already_in_cart.totalprice = already_in_cart.totalprice + int(addtocart.qty) * int(singleproductdetails.price)
                        already_in_cart.save()
                        singleproductdetails.stock = singleproductdetails.stock - int(addtocart.qty)
                        singleproductdetails.save()
                        return redirect('cart')
                    else:    
                        addtocart.save()
                        singleproductdetails.stock = singleproductdetails.stock - int(addtocart.qty)
                        singleproductdetails.save() 
                        # singleproductdetails.stock = singleproductdetails.stock + int(addtocart.qty)
                        # singleproductdetails.save()
                        return render(request,'product.html',{'prodetails':singleproductdetails,'loggedin':loggedinuser})
        else:
            return redirect('login')
    else:
        if 'email' in request.session:
            return render(request,'product.html',{'prodetails':singleproductdetails,'loggedin':True})
        return render(request,'product.html',{'prodetails':singleproductdetails})


def register(request):
    if request.method == 'POST':
        regdata = registration()
        regdata.name = request.POST['name']
        regdata.email  = request.POST['email']
        regdata.mob  = request.POST['mob']
        regdata.add  = request.POST['add']
        regdata.password  = request.POST['password']
        registeruser = registration.objects.filter(email = request.POST['email'])
        if registeruser:
            return render(request,'register.html',{'already':"This email is already register"})
        else:
            regdata.save()
            return redirect('login')
    else:
        return render(request,'register.html')
    
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned
from django.core.mail import send_mail

def login(request):
    if request.method == 'POST':
        try:
            loginuser = registration.objects.get(email = request.POST['email'])
            if loginuser.password == request.POST['password']:
                request.session['email'] = loginuser.email
                send_mail(
                    'Verification Mail',
                    'This mail is for verification pupose, dont replay to this mail',
                    'dharamatholiya1116@gmail.com',
                    [loginuser.email],
                    fail_silently = False
                )
                return redirect('index')
            else:
                return render(request,'login.html',{'invalid':"Password invalid..."})
        except ObjectDoesNotExist:
            return render(request,'login.html',{'notregistered':"you have to registered first!!"})
        except MultipleObjectsReturned:
            return render(request,'login.html',{'registeredmultitime':"You have registered multi times..!!"})
    else:
        return render(request,'login.html')    
    
def logout(request):
    del request.session['email']
    return redirect('index')

def profile(request):
    if 'email' in request.session:
        data = registration.objects.get(email = request.session['email'])
        if request.method == 'POST':
            data.name = request.POST['name']
            data.email = request.POST['email']
            data.add = request.POST['add']
            data.mob = request.POST['mob']
            data.save()
            return render(request,'profile.html',{'loggedin':data})
        else:
            return render(request,'profile.html',{'loggedin':data})
    else:
        return redirect('login')  

def cartview(request):
    if 'email' in request.session:
        loggedin_user = registration.objects.get(email = request.session['email'])
        cartdata = cart.objects.filter(userid = loggedin_user,orderid = '0')
        grand_total = 0
        for i in cartdata:
            grand_total += int(i.totalprice)
        if 'out_of_stock' in request.session:
            del request.session['out_of_stock']
            return render(request,'cart.html',{'loggedin':loggedin_user,'out_of_stock':'stock unavailable..!','cartdata':cartdata,'grandtotal':grand_total})
        else:    
            return render(request,'cart.html',{'loggedin':loggedin_user,'cartdata':cartdata,'grandtotal':grand_total})
    else:
        return redirect('login')               
    

def plusitem(request,id):
    cartitem = cart.objects.get(id =id)
    if cartitem.proid.stock <=0:
        request.session['out_of_stock'] = True
        return redirect('cart')
    else:
        cartitem.qty = cartitem.qty +1
        cartitem.totalprice = cartitem.totalprice + cartitem.proid.price

        cartitem.save()    
        proitem = product.objects.get(id = cartitem.proid.pk)
        proitem.stock = proitem.stock -1
        proitem.save()  
        return redirect('cart')

def minusitem(request,id):
    cartitem = cart.objects.get(id = id)
    if cartitem.qty <=1:
        cartitem.delete()
        return redirect('cart')
    else:
        cartitem.qty = cartitem.qty - 1
        cartitem.totalprice = cartitem.totalprice - cartitem.proid.price
        cartitem.save()
        proitem = product.objects.get(id = cartitem.proid.pk)
        proitem.stock = proitem.stock + 1
        proitem.save()
        return redirect('cart')    
    
def productremove(request,id): 
       cartitem = cart.objects.get(id= id)
       itemofcart = cartitem.qty
       proitem = product.objects.get(id = cartitem.proid.pk)
       proitem.delete()
       proitem.stock = proitem.stock +itemofcart
       proitem.save()  
       return redirect('cart')

def allproductremove(request):
    loggedin = registration.objects.get(email = request.session['email'])
    cartdata = cart.objects.filter(userid = loggedin,orderid = '0')

    for i in cartdata:
        prodata = product.objects.get(id = i.proid.id)
        prodata.stock = prodata.stock + i.qty
        prodata.save()
    cartdata.delete()
    return redirect('cart')


def checkout(request):
    if 'email' in request.session:
        loggedin = registration.objects.get(email = request.session['email'])
        checkoutdata = cart.objects.filter(userid = loggedin,orderid = '0')
        totalprice = 0
        for i in checkoutdata:
            totalprice += i.totalprice
        if request.method == 'POST':
            payment_mode = request.POST['paymentvia']
            if payment_mode == 'cod':
                for i in checkoutdata:
                    storeorder = order()
                    storeorder.proid = i.proid
                    storeorder.userid = loggedin 
                    storeorder.add = request.POST['add']
                    storeorder.city = request.POST['city']
                    storeorder.state = request.POST['state']
                    storeorder.pin = request.POST['pin']
                    storeorder.mob = request.POST['mob'] 
                    storeorder.Grand_price = totalprice 
                    storeorder.payment_mode = request.POST['paymentvia']
                    storeorder.Total_price = totalprice
                    storeorder.qty = i.qty
                    storeorder.transaction_id = 'cod'
                    storeorder.save()
                    latest_order_id = order.objects.latest('id')
                    i.orderid = latest_order_id.pk
                    i.save() 
            else:
                request.session['amount'] = totalprice
                request.session['add'] = request.POST['add'] 
                request.session['city'] = request.POST['city']
                request.session['state'] = request.POST['state'] 
                request.session['pin'] = request.POST['pin']
                request.session['mob'] = request.POST['mob']   
                return redirect('razorpayment')
                    
        return render(request,'checkout.html',{'loggedin':loggedin,'checkout':checkoutdata,'totalprice':totalprice})        
    
def orderhistory(request):
       if 'email' in request.session:
            loggedin = registration.objects.get(email = request.session['email']) 
            orderhis = order.objects.filter(userid = loggedin) 
            return render(request,'orderhistory.html',{'loggedin': loggedin,'order_history':orderhis})
       else:
           return redirect('login')
       
RAZOR_KEY_ID = 'rzp_test_F9gRSjaJozWYhc'
RAZOR_KEY_SECRET = 'tSdNYZSrIL2xf86MVtj4J3MY'

import razorpay

razorpay_client = razorpay.Client(auth=(RAZOR_KEY_ID, RAZOR_KEY_SECRET))

def razorpayment(request):
    currency = 'INR'
    amount = request.session['amount'] * 100
     
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))

    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'http://127.0.0.1:8000/paymenthandler/'
    return render(request,'razorpay.html',{'razorpay_merchant_key': RAZOR_KEY_ID,'razorpay_amount': amount,
                                           'currency':currency,'razorpay_order_id':razorpay_order_id,'callback_url': callback_url})

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

@csrf_exempt
def paymenthandler(request):
    if request.method == 'POST':
        try:
            print(000000000000000000)
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            print(11111111111)
            params_dict = {
                'razorpay_payment_id': payment_id,
                'razorpay_order_id': razorpay_order_id,
                'razorpay_signature': signature
            }
            print(3333333333333333333333333)
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            amount = request.session['amount'] * 100
            razorpay_client.payment.capture(payment_id, amount)
            print("============")
            print("transaction id:",payment_id)
            print("=============")
            loggedin_user = registration.objects.get(email = request.session['email'])
            cartdata = cart.objects.filter(userid = loggedin_user,orderid = 0)
            print(4444444444444444444444444444444)
            for i in cartdata:
                order_store = order()
                order_store.proid = i.proid
                order_store.userid = loggedin_user
                order_store.Total_price = i.totalprice
                order_store.payment_mode = 'ONLINE'
                order_store.transaction_id = payment_id
                order_store.orderid = razorpay_order_id
                order_store.add = request.session['add']
                order_store.city = request.session['city']
                order_store.state = request.session['state']
                order_store.pin = request.session['pin']
                order_store.mob = request.session['mob']
                order_store.save()
                latest_row = order.objects.latest('id')
                i.orderid = latest_row.id
                i.save()
            return redirect('index')
            print(5555555555555555555555555)
        except Exception as e:
            print(e)
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()    



# ---------------------Django rest-----------------------

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serialize import Serialize_registers

@api_view(['GET'])
def random_api_check(request):
    return Response({'1':'This is 1st data',
                     'second':'api made successfully',
                     3:3})


@api_view(["GET"])
def api_view_of_register(request):
    register_data = registration.objects.all()
    final = Serialize_registers(register_data, many= True)
    return Response(final.data)

@api_view(['GET'])
def api_view_to_store(request):
    register_data = request.data
    final = Serialize_registers(data = register_data)
    if final.is_valid():
        final.save()
        return Response("Data stored succesdully")
    else:
        return Response("Data failed to store")