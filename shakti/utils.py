import json
from .models import *
# we are creating this function so we can paste this code for the anonyoumous user in the else part of all the views
# here we store our data in cookie and reterive the information
def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])#by this we can get our cookie , our cookie is in string so we need to parse it
    except:
        cart = {}
        print('CART:', cart)

    items = []
    order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
    cartItems = order['get_cart_items']

# so here get get_cart_total and get_cart_items is an attribute which we call in our templates and that is cart.html
    for i in cart:
      try:
        cartItems += cart[i]['quantity']#updating the cartitem and it get thrown in contect dictionary
        product = Product.objects.get(id=i)# this will return product only if product is in cookie for some reason if product is deleted in cookie we see an error message, but we don't want so we use try
        total = (product.price * cart[i]['quantity'])

        order['get_cart_total'] += total
        order['get_cart_items'] += cart[i]['quantity']

        item = {
            'id':product.id,
            'product':{'id':product.id,'name':product.name, 'price':product.price,
            'imageURL':product.imageURL}, 'quantity':cart[i]['quantity'],
            'digital':product.digital,'get_total':total,
            }
        items.append(item)#here we are basically adding this item the above item dictionary
# these are for teh cart page item, price , quantity, total , all we get this from our python dictiortonary in console which is created by clicking on add to cart button
        if product.digital == False:
            order["shipping"] = True
      except:
          pass

    return {'cartItems':cartItems ,'order':order, 'items':items}






def cartData(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		cookieData = cookieCart(request)
		cartItems = cookieData['cartItems']
		order = cookieData['order']
		items = cookieData['items']

	return {'cartItems':cartItems ,'order':order, 'items':items}








def guestOrder(request, data):
	name = data['form']['name']
	email = data['form']['email']

	cookieData = cookieCart(request)
	items = cookieData['items']

	customer, created = Customer.objects.get_or_create(
			email=email,
			)
	customer.name = name
	customer.save()

	order = Order.objects.create(
		customer=customer,
		complete=False,
		)

	for item in items:
		product = Product.objects.get(id=item['id'])
		orderItem = OrderItem.objects.create(
			product=product,
			order=order,
			quantity=item['quantity'],
		)
	return customer, order
