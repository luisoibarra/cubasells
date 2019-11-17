from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
def validate_positive(number):
    if number < 0:
        raise ValidationError(f'{number} must be a positive number')

class Image(models.Model):
    
    image = models.ImageField(name = 'Image', upload_to='static/images', default='static/images/default/defaut.png')

class Tag(models.Model):
    
    tag = models.CharField(name='Tag', max_length=50)

class Entity(models.Model):
    
    name = models.CharField(name='Name',max_length=150)
    
    description = models.CharField(name="Description",max_length=400, default='',help_text='Description',blank=True)
    
    create_date = models.DateTimeField(name="Create Date",auto_now=False, auto_now_add=True)

    images = models.ManyToManyField(Image, related_name='Images',blank=True)
    
    tags = models.ManyToManyField(Tag, related_name='Tags',blank=True)
    # def __str__(self):
    #     return self.name
    
class RealEntity(Entity):
    
    email = models.EmailField(name='Email', max_length=254)
    
    phone = models.IntegerField(name='Phone number',null=True,validators=(validate_positive,))

class BankAccount(models.Model):
    
    bank_account = models.IntegerField(name='Bank account',validators=(validate_positive,))
    
class User(RealEntity):
    
    bank_accounts = models.ManyToManyField(BankAccount, through='Buyer',through_fields=('User','Account'))

class Buyer(models.Model):
    
    user = models.ForeignKey(User,name = 'User', on_delete=models.CASCADE)
    
    account = models.ForeignKey(BankAccount,name = 'Account', on_delete=models.CASCADE)
    
class Store(RealEntity):
    
    owner = models.ForeignKey(User, name='Owner', on_delete=models.CASCADE)   
    
    bank_account = models.ForeignKey(BankAccount,name = 'Bank account', on_delete=models.CASCADE) 

class Product(Entity):
    
    unit_price = models.FloatField(name='Price per unit',validators=(validate_positive,))
    
    store_amount = models.IntegerField(name = "Store Amount",validators=(validate_positive,))
    
    store = models.ForeignKey(Store,name = 'Store',default=-1, on_delete=models.CASCADE)
    
    buy_product = models.ManyToManyField(Buyer, through='Buy', through_fields=('Selled Product','Buyer'))

class Buy(models.Model):

    selled_product = models.ForeignKey(Product, name='Selled Product', on_delete=models.CASCADE)

    buyer = models.ForeignKey(Buyer, name='Buyer', on_delete=models.CASCADE)
    
    buy_date = models.DateTimeField(name= 'Buy Date', auto_now=False, auto_now_add=True)

    amount = models.IntegerField(name = 'Amount',validators=(validate_positive,))

