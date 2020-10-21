from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import cookieCart ,cartData,guestOrder
import razorpay
# Create your views here.
# we use . becoz views and models are in the same directory
# def store(request):
#     if request.user.is_authenticated:
#         customer = request.user.customer  #grabbing the name of customer#here we are return the string representatin of customer model and that is name
#         order, created = Order.objects.get_or_create(customer=customer, complete=False)# creating an order related to that customer, pehla order is 1, doosra order is 2... and so on , in one order there can be multiple items
#         items = order.orderitem_set.all()#in order object we have also shipping method , so we can render it in templates
#         cartItems = order.get_cart_items#here we are grabbing the total number of items, us cart wale symbol ke liye
#           #here we are grabbing ki is order mai kitne items hai
#     else:#this is logic for the anonymouse user which is in function cookiecart and we access it here in all the views
#         cookieData = cookieCart(request)
#         cartItems = cookieData['cartItems']
#         # order = cookieData['order']
#         # items = cookieData['items']
#     products = Product.objects.all()
#     context ={'products':products,'cartItems':cartItems}
#     return render(request,'store/store.html',context)
#
# def cart(request):
#     if request.user.is_authenticated:
#         customer = request.user.customer# this is one to one relationship this means to grab the authorized customer username
#         order, created = Order.objects.get_or_create(customer=customer, complete=False)
#         # we do this way beacuse we either want to create an order or grab an order if it exist
#         #get or create basically first query an object to grab it if it does not exist it will create that object with certain values
#         #get_or_create means either create it for find it
#
#         items = order.orderitem_set.all()# basically we are tellling that us particular order se related saare order items le aao
#         cartItems = order.get_cart_items# cartItems ko hmne saare views mai likha hai kyoki , hme cart icon ki value saare page mai update krni hai aur vo value hai cartItem
#         # here we are able to query child object by setting the parent value(order), so by this we will able to grab all the attributes of orderitem related to that order
#
#     #     # it will grab all the orderitem with order as a parent
#     else:
#
#         cookieData = cookieCart(request)
#         cartItems = cookieData['cartItems']
#         order = cookieData['order']
#         items = cookieData['items']
#
#
#     context ={'items':items, 'order':order, 'cartItems':cartItems}
#     return render(request,'store/cart.html',context)
#
# def checkout(request):
#     if request.user.is_authenticated:
#         customer = request.user.customer# this is one to one relationship this means to grab the authorized customer username
#         order, created = Order.objects.get_or_create(customer=customer, complete=False)
#         # we do this way beacuse we either want to create an order or grab an order if it exist
#         #get or create basically first query an object to grab it if it does not exist it will create that object with certain values
#         #get_or_create means either create it for find it
#         #
#         items = order.orderitem_set.all()
#         cartItems = order.get_cart_items# this is used to print the cart item in the cart icon in the chekout page
#         # here we are able to query child object by setting the parent value(order), so by this we will able to grab all the attributes of order
#         # it will grab all the orderitem with order as a parent
#     else:
#
#         cookieData = cookieCart(request)
#         cartItems = cookieData['cartItems']
#         order = cookieData['order']
#         items = cookieData['items']
# # so here get get_cart_total and get_cart_items is an attribute which we call in our templates and that is cart.html
#
#     context ={'items':items, 'order':order, 'cartItems':cartItems}
#     return render(request,'store/checkout.html',context)

def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    # order = data['order']
    # items = data['items']

    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'shakti/store.html', context)


def cart(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'shakti/cart.html', context)

def checkout(request):



    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']


    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'shakti/checkout.html', context)


# cart.js se hmne information fetch ki , ki button click ho to kya krna hai, us information ko hm is views.py mai laa rhe hai
def updateItem(request):
    data = json.loads(request.body)#we are passing the data here, this data is coming from cart.js updateUserOrder functions
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)
# here we are actually grabbing the details
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
# the reason we create get_or_create is we need to change the value of order if it exist, here we want to change the quantity of the order

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':#this we add in down arrow so as down arrow is clicked we get an info from js through csrf and we reduce the item
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
# if the item is less than 0 we will remove that item
    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
#so if user is authenticated we process there information and if they are not authenticated logic in the else section
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # total = float(data['form']['total'])
        # order.transaction_id = transaction_id
        #
        #
        # if total == order.get_cart_total:
        #     order.complete = True
        # order.save()
        #ye upar wala code jo comment hua hai wo authenticated aur non authenticated user dono ke liye hai to ye sbse nich jayega , if else mai nhi rahega
# here we are checking that order we pass in front end is matching to the backend , becoz some fraud manipulate the data of frontend with little knowledge of javascript
#but here regardless of you total is correct or not we still save it , but you can apply your own logic
        # if order.shipping == True:
        #     ShippingAddress.objects.create(
        #     customer=customer,
        #     order=order,
        #     address=data['shipping']['address'],
        #     city=data['shipping']['city'],
        #     state=data['shipping']['state'],
        #     zipcode=data['shipping']['zipcode'],
        #     )
        # ye code niche gya hai login aur anonymous user dono ke liye hai
    else:
        customer, order = guestOrder(request, data)
        # print('User is not logged in')
        #
        #
        # print('COOKIES:', request.COOKIES)
        # name = data['form']['name']
        # email = data['form']['email']
        #
        # cookieData = cookieCart(request)
        # items = cookieData['items']
        #
        # customer, created = Customer.objects.get_or_create(
        #         email=email,
        #         )#here we are creating the Customer
        #         #so when we have guest user who want to shop but dosen't want to create an account, we can do this just by taking his email , so we can get that how many time this customer has done shop with us
        # customer.name = name# we are taking his name also but if he wants to change his name after , that is why we are taking it off from get and create method
        # customer.save()
        #
        # order = Order.objects.create(#creating the order
        #     customer=customer,
        #     complete=False,
        #     )
        # #now we are going to loop through all of these items right here remember it is just the list of dictionary right now
        # #we need to acctually add this items to the database and then create them and then attach them to this order object which we just created
        #
        # for item in items:
        #     product = Product.objects.get(id=item['id'])
        #     orderItem = OrderItem.objects.create(
        #         product=product,
        #         order=order,
        #         quantity=item['quantity'],
        #     )

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)
