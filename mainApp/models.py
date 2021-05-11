from django.conf import settings
from django.db import models
from django.shortcuts import reverse

# Create your models here.

CATEGORY_CHOICES = (
    ('LEG', 'Légume'),
    ('FRU', 'Fruit'),
    ('COS', 'Cosmétique'),
)
class Category(models.Model):
    name = models.CharField(choices=CATEGORY_CHOICES, max_length=5)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("mainApp:cat_products", kwargs={
            'catname':self.name
        })


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()       
    slug = models.SlugField()
    discount_price = models.FloatField(blank=True, null=True) 
    pic = models.ImageField(blank=True, null=True, upload_to='products')  
    liked = models.IntegerField(default=0)
    cat = models.ForeignKey(Category, blank=True,default=None, on_delete = models.CASCADE)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("mainApp:product", kwargs={
            'slug':self.slug
        })
    def get_add_to_cart_url(self):
        return reverse("mainApp:add_to_cart", kwargs={
            'slug':self.slug
        })
    def get_remove_from_cart_url(self):
        return reverse("mainApp:remove_from_cart", kwargs={
            'slug':self.slug
        })

TYPE_PANIER = (
    ('PET', 'Petit'),
    ('MOY', 'Moyen'),
    ('GRA', 'Grand'),
)
class Panier(models.Model):
    type = models.CharField(choices=TYPE_PANIER, max_length=5)
    price = models.FloatField()   
    poids = models.IntegerField(blank=True, null=True) 
    items = models.ManyToManyField(Item)
    slug = models.SlugField()
    discount_price = models.FloatField(blank=True, null=True) 
    liked = models.IntegerField(default=0)
    pic = models.ImageField(blank=True, null=True, upload_to='products')  

    def __str__(self):
        return self.type + " panier"
    def get_absolute_url(self):
        return reverse("mainApp:panier", kwargs={
            'slug':self.slug
        })
    def get_add_to_cart_url(self):
        return reverse("mainApp:add_panier_to_cart", kwargs={
            'slug':self.slug
        })
    
    def get_remove_from_cart_url(self):
        return reverse("mainApp:remove_panier_from_cart", kwargs={
            'slug':self.slug
        })
    

class BillingAdddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    streetaddress = models.CharField(max_length=100)
    postcodezip =  models.CharField(max_length=15)
    ville =  models.CharField(max_length=30)

    def __str__(self):
        return self.user.username
    

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"
    def get_total_item_price(self):
        return self.quantity * self.item.price
    def get_total_panier_price(self):
        return self.quantity * self.panier.price
    
    def get_total_discount_price_price(self):
        return self.quantity * self.item.discount_price
    def get_total_discount_panier_price_price(self):
        return self.quantity * self.panier.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_price_price()
    def get_amount_panier_saved(self):
        return self.get_total_panier_price() - self.get_total_discount_panier_price_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_price_price()
        return self.get_total_item_price() 
    def get_final_panier_price(self):
        if self.panier.discount_price:
            return self.get_total_discount_panier_price_price()
        return self.get_total_panier_price()     



class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    code_promo = models.CharField(max_length=15, blank=True, null=True)
    livraison = models.FloatField(default=0.00)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date  = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_adddress = models.ForeignKey(BillingAdddress, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    def isCodePromoValid(self):
        validCodes = ['code1', 'code2', 'code3']
        if self.code_promo and self.code_promo in validCodes:
            return True
        return False 

    def get_total_HT(self):
        total = 0
        for order_item in self.items.all():
            if order_item.item:
                total+=order_item.get_final_price()
            elif order_item.panier:
                total+=order_item.get_final_panier_price()
        return total

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            if order_item.item:
                total+=order_item.get_final_price()
            elif order_item.panier:
                total+=order_item.get_final_panier_price()
        if self.isCodePromoValid():
            total-=total*0.1
        return total+self.livraison

    
