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
        raise ValidationError(f'{number} must be a positive number')

class Image(models.Model):
    
    image = models.ImageField(name = 'Image', upload_to='static/images', default='static/images/default/defaut.png')

class Tag(models.Model):
    
    tag = models.CharField(name='Tag', max_length=50,unique=True)

class Entity(models.Model):
    
    description = models.CharField(name="Description",max_length=400, default='',help_text='Description',blank=True)
    
    images = models.ManyToManyField(Image, name='Images',related_name='Images',blank=True)
    
    tags = models.ManyToManyField(Tag, name='Tags',related_name='Tags',blank=True)
    
class RealEntity(Entity):
    
    phone = models.IntegerField(name='Phone',null=True,validators=(validate_positive,),blank=True)

class BankAccount(models.Model):
    
    bank_account = models.IntegerField(name='Bank account',validators=(validate_positive,))
    
class MyUser(RealEntity):
    
    bank_accounts = models.ManyToManyField(BankAccount, name = 'Accounts',through='Buyer',through_fields=('MyUser','Account'))
    
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
        
 
@receiver(post_save,sender = User)
def create_user_profile(sender,instance,created,**kwarg):
    if created:
        MyUser.objects.create(user = instance)

@receiver(post_save,sender = User)
def save_user_profile(sender,instance,**kwarg):
    instance.myuser.save()

class Buyer(models.Model):
    
    user = models.ForeignKey(MyUser,name = 'MyUser', on_delete=models.CASCADE)
    
    account = models.ForeignKey(BankAccount,name = 'Account', on_delete=models.CASCADE)
    
class Store(RealEntity):
    
    name = models.CharField(name='Name',max_length=150)
    
    create_date = models.DateTimeField(name="Create Date",auto_now=False, auto_now_add=True)

    email = models.EmailField(name='Email', max_length=254)
    
    owner = models.ForeignKey(MyUser, name='Owner', on_delete=models.CASCADE)   
    
    bank_account = models.ForeignKey(BankAccount,name = 'Bank account', on_delete=models.CASCADE) 

class Product(Entity):
    
    unit_price = models.FloatField(name='Price per unit',validators=(validate_positive,))
    
    store_amount = models.IntegerField(name = "Store Amount",validators=(validate_positive,))
    
    store = models.ForeignKey(Store,name = 'Store',default=-1, on_delete=models.CASCADE)
    
    buy_product = models.ManyToManyField(Buyer, through='Buy', through_fields=('Selled Product','Buyer'))
    
    visible = models.BooleanField(name='Visible',default=True)

class Buy(models.Model):

    selled_product = models.ForeignKey(Product, name='Selled Product', on_delete=models.CASCADE)

    buyer = models.ForeignKey(Buyer, name='Buyer', on_delete=models.CASCADE)
    
    buy_date = models.DateTimeField(name= 'Buy Date', auto_now=False, auto_now_add=True)

    amount = models.IntegerField(name = 'Amount',validators=(validate_positive,))

class Chat(models.Model):
    
    sender_user = models.ForeignKey(MyUser, related_name='sender_table', on_delete=models.CASCADE)
    
    reciever_user = models.ForeignKey(MyUser,related_name='reciever_table', on_delete=models.CASCADE)
    
    date = models.DateTimeField(name='Date', auto_now=False, auto_now_add=True)
    
    message = models.CharField(name='Message', max_length=1000)
    
    type_of_message = models.CharField(name='type',default='N',max_length=15,choices=[('N','Normal'),('I','Important'),('W','Warning')])
    
class Offer(models.Model):

    price = models.FloatField(name='Price',validators=(validate_positive,))
    
    name = models.CharField(name='Offer name', max_length=50)
    
    description = models.CharField(name='Offer description', max_length=150)
    
    buy_offer = models.ManyToManyField(Buyer,through='BuyOffer',through_fields=('Offer','Buyer'))

class SubOffer(models.Model):
    
    product_offer = models.ForeignKey(Product, name = 'Product offer',on_delete=models.CASCADE)
    
    amount = models.IntegerField(name='Amount', validators=(validate_positive,))
    
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)

class BuyOffer(models.Model):
    
    buyer = models.ForeignKey(Buyer, name='Buyer', on_delete=models.CASCADE)
    
    offer = models.ForeignKey(Offer,name='Offer', on_delete=models.CASCADE)
    
    buy_date = models.DateTimeField(name='Buy Date', auto_now=False, auto_now_add=True)
    
class Auction(models.Model):
    
    winner = models.OneToOneField(Buyer, name='Winner', on_delete=models.CASCADE, blank=True,null=True)
    
    offered = models.ForeignKey(Offer, name='Offered', on_delete=models.CASCADE)
    
    initial_date = models.DateTimeField(name='Initial Date', auto_now=False, auto_now_add=False)
    
    duration = models.IntegerField(name='Duration(sec)',validators=(validate_positive,))
    
    money_pool = models.IntegerField(name='Money',validators=(validate_positive,))