from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
def validate_positive(number):
    if number < 0:
        raise ValidationError('%(number) must be a positive number',code='invalid number',params={'number':number,})

class Image(models.Model):
    
    name = models.CharField(name='Name',max_length=200)
    
    image = models.ImageField(name = 'Image', upload_to='images',default='default.jpg')
    
    # owner = models.ForeignKey('project.MyUser', name="Owner", on_delete=models.CASCADE)

class Tag(models.Model):
    
    tag = models.CharField(name='Tag', max_length=50,unique=True)
    
    def __str__(self):
        return self.Tag

class MyUser(User):
     
    description = models.CharField(name="Description",max_length=400, default='',help_text='Description',blank=True)
    
    images = models.ManyToManyField(Image, name='Images',related_name='Images_User',blank=True)
    
    tags = models.ManyToManyField(Tag, name='Tags',related_name='Tags_User',blank=True)
    
    phone = models.IntegerField(name='Phone',null=True,validators=(validate_positive,),blank=True)
    
    cart = models.OneToOneField('project.ShoppingCart',name='Cart',on_delete=models.CASCADE)
    
    def __str__(self):
        return self.username
        
class BankAccount(models.Model):
    
    user = models.ForeignKey(MyUser,name = 'MyUser', on_delete=models.CASCADE)
    
    account = models.IntegerField(name='Account',validators=(validate_positive,))
    
    class Meta:
        unique_together = ('MyUser','Account',)        
  
    def __str__(self):
        return f'{self.MyUser} {self.Account}'
    
class Store(models.Model):
    
    name = models.CharField(name='Name',max_length=150)
    
    create_date = models.DateTimeField(name="Create_Date",auto_now=False, auto_now_add=True)

    email = models.EmailField(name='Email', max_length=254)
    
    owner = models.ForeignKey(MyUser, name='Owner', on_delete=models.CASCADE)   
    
    description = models.CharField(name="Description",max_length=400, default='',help_text='Description',blank=True)
    
    images = models.ManyToManyField(Image, name='Images',related_name='Images_Store',blank=True)
    
    tags = models.ManyToManyField(Tag, name='Tags',related_name='Tags_Store',blank=True)
    
    phone = models.IntegerField(name='Phone',null=True,validators=(validate_positive,),blank=True)
    
    bank_account = models.ForeignKey(BankAccount,name = 'Bank_Account', on_delete=models.CASCADE) 
    
    def __str__(self):
        return self.Name
    
class Product(models.Model):
    
    # unit_price = models.FloatField(name='Price_per_unit',validators=(validate_positive,))
    
    store_amount = models.IntegerField(name = "Store_Amount",validators=(validate_positive,))
    
    store = models.ForeignKey(Store,name = 'Store',default=-1, on_delete=models.CASCADE)
    
    # buy_product = models.ManyToManyField(Buyer, through='Buy', through_fields=('Selled Product','Buyer'))
    
    # visible = models.BooleanField(name='Visible',default=True)
    
    name = models.CharField(name='Name',max_length=150)
        
    description = models.CharField(name="Description",max_length=400, default='',help_text='Description',blank=True)
    
    images = models.ManyToManyField(Image, name='Images',related_name='Images_Product',blank=True)
    
    tags = models.ManyToManyField(Tag, name='Tags',related_name='Tags_Product',blank=True)
    
    def __str__(self):
        return f'{self.Name} in {self.Store.Name}'
    
class Chat(models.Model):
    
    sender_user = models.ForeignKey(MyUser, related_name='sender_table', on_delete=models.CASCADE)
    
    reciever_user = models.ForeignKey(MyUser,related_name='reciever_table', on_delete=models.CASCADE)
    
    date = models.DateTimeField(name='Date', auto_now=False, auto_now_add=True)
    
    message = models.CharField(name='Message', max_length=1000)
    
    type_of_message = models.CharField(name='type',default='N',max_length=15,choices=[('N','Normal'),('I','Important'),('W','Warning')])
    
    def __str__(self):
        return f'{self.sender_user.username} -> {self.reciever_user.username}; {self.Date}'
    
class SubOffer(models.Model):
    
    product_offer = models.ForeignKey(Product, name = 'Product_offer',on_delete=models.CASCADE)
    
    amount = models.IntegerField(name='Amount', validators=(validate_positive,))
    
    def __str__(self):
        return f'{self.Product_offer.Name}:{self.Amount}'

class Offer(models.Model):

    price = models.FloatField(name='Price',validators=(validate_positive,))
    
    name = models.CharField(name='Offer_name', max_length=50)
    
    description = models.CharField(name='Offer_description', max_length=150)
    
    store = models.ForeignKey(Store,name = 'Store', default = -1, on_delete=models.CASCADE)
    
    buy_offer = models.ManyToManyField(BankAccount,through='BuyOffer',through_fields=('Offer','Buyer'))
    
    images = models.ManyToManyField(Image, name='Images',related_name='Images_Offer',blank=True)
    
    tags = models.ManyToManyField(Tag, name='Tags',related_name='Tags_Offer',blank=True)

    suboffer = models.ManyToManyField(SubOffer,name='Suboffer',related_name='Suboffer_offer')
    
    def __str__(self):
        return f'{self.Offer_name}'

class BuyOffer(models.Model):
    
    buyer = models.ForeignKey(BankAccount, name='Buyer', on_delete=models.CASCADE)
    
    offer = models.ForeignKey(Offer,name='Offer', on_delete=models.CASCADE)
    
    buy_date = models.DateTimeField(name='Buy_Date', auto_now=False, auto_now_add=True)
    
    amount = models.IntegerField(name='Amount',validators=(validate_positive,))
    
    def __str__(self):
        return f'{self.Buyer.MyUser.username} -> {self.Offer.Offer_name}; {self.Buy_Date}'
    
class Auction(models.Model):
    
    winner = models.OneToOneField(BankAccount, name='Winner', on_delete=models.CASCADE, blank=True,null=True)
    
    offered = models.ForeignKey(Offer, name='Offered', on_delete=models.CASCADE)
    
    initial_date = models.DateTimeField(name='Initial_Date', auto_now=False, auto_now_add=False)
    
    duration = models.IntegerField(name='Duration_in_sec',validators=(validate_positive,))
    
    money_pool = models.IntegerField(name='Money',validators=(validate_positive,))
    
    def __str__(self):
        return f'{self.Offered.name} {self.Money}'

class ShoppingCart(models.Model):
    pass    

class ShoppingOffer(models.Model):
    
    offer = models.ForeignKey(Offer,on_delete=models.CASCADE,name='Offer')
    
    amount = models.PositiveIntegerField(name='Amount')
    
    cart = models.ForeignKey(ShoppingCart, name='Cart', on_delete=models.CASCADE)