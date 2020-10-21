from django.db import models
from django.contrib.auth.models import User
# this django default user model
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)
# one to one relationship means that User can only  have one customer and customer can have only one User
#on_delete= models.CASCADE means we just want to delete this item if the user item is deleted

    def __str__(self):
        return self.name
#this is the value we see in our admin panel


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=False, blank=True)
    image = models.ImageField(null=True, blank=True)
# digital is boolean value because if the product is digital so we don't want to ship it,so it is either true or False

    def __str__(self):
        return self.name

    # property decorator is used to access the function as attribute not as a method

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
# if there is no images we cannot get the url of image so we get an error , in order to remove
# error we need to use this property decorator which tell us if there is image in the url query this otherwise query otherwise query url=''


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    # amount = models.IntegerField(default=0)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
# ForeignKey is many to one relationship , here it means that Customer can have multiple Order
# Foreign key is way to connect a record from one model  with record from another model
# BAsically yaha foreign key is liye use ki gyi hai taki Authorised Customer se Connected order aa jaye
# complete = boolean=false means we can add product to the cart
#on_delete=models.SET_NULL, here we did not use cascade becoz on using cascade that means if user is deleted than his item get also deleted
# here  we use SET_NULL which means if user deleted order should not be deleted

    def __str__(self):
        return str(self.id)
# here our id is integer so here we are converting it into string becoz we have to return a string
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping
# basically this telling if there is no digital product then show up the shiping fields

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()# here we are accessing th element of order items
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity=models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
#single order can have multiple order items


    def __str__(self):
        return self.product.name


    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
# it wil create the total, then we grab this


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
