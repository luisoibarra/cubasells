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
    
    def __str__(self):
        return self.Tag

class Entity():
    
    description = models.CharField(name="Description",max_length=400, default='',help_text='Description',blank=True)
    
    images = models.ManyToManyField(Image, name='Images',related_name='Images',blank=True)
    
    tags = models.ManyToManyField(Tag, name='Tags',related_name='Tags',blank=True)
    
class RealEntity(Entity):
    
    phone = models.IntegerField(name='Phone',null=True,validators=(validate_positive,),blank=True)
    
class BankAccount(models.Model):
    
    bank_account = models.IntegerField(name='Bank_account',validators=(validate_positive,))
    
    def __str__(self):
        return str(self.Bank_account)
    
class MyUser(User):
     
    bank_accounts = models.ManyToManyField(BankAccount, name = 'Accounts', related_name='Accounts_User'\
        ,through='Buyer',through_fields=('MyUser','Account'),blank=True)
    
    description = models.CharField(name="Description",max_length=400, default='',help_text='Description',blank=True)
    
    images = models.ManyToManyField(Image, name='Images',related_name='Images_User',blank=True)
    
    tags = models.ManyToManyField(Tag, name='Tags',related_name='Tags_User',blank=True)
    
    phone = models.IntegerField(name='Phone',null=True,validators=(validate_positive,),blank=True)
    
    def __str__(self):
        return self.username
        
class Buyer(models.Model):
    
    user = models.ForeignKey(MyUser,name = 'MyUser', on_delete=models.CASCADE)
    
    account = models.ForeignKey(BankAccount,name = 'Account', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.MyUser} {self.Account}'
    
class Store(models.Model):
    
    name = models.CharField(name='Name',max_length=150)
    
    create_date = models.DateTimeField(name="Create Date",auto_now=False, auto_now_add=True)

    email = models.EmailField(name='Email', max_length=254)
    
    owner = models.ForeignKey(MyUser, name='Owner', on_delete=models.CASCADE)   
    
    description = models.CharField(name="Description",max_length=400, default='',help_text='Description',blank=True)
    
    images = models.ManyToManyField(Image, name='Images',related_name='Images_Store',blank=True)
    
    tags = models.ManyToManyField(Tag, name='Tags',related_name='Tags_Store',blank=True)
    
    phone = models.IntegerField(name='Phone',null=True,validators=(validate_positive,),blank=True)
    
    bank_account = models.ForeignKey(BankAccount,name = 'Bank account', on_delete=models.CASCADE) 
    
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
    
# class Buy(models.Model):

#     selled_product = models.ForeignKey(Product, name='Selled Product', on_delete=models.CASCADE)

#     buyer = models.ForeignKey(Buyer, name='Buyer', on_delete=models.CASCADE)
    
#     buy_date = models.DateTimeField(name= 'Buy Date', auto_now=False, auto_now_add=True)

#     amount = models.IntegerField(name = 'Amount',validators=(validate_positive,))
    
#     def __str__(self):
#         return self.Buyer.Name

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
    
    buy_offer = models.ManyToManyField(Buyer,through='BuyOffer',through_fields=('Offer','Buyer'))
    
    images = models.ManyToManyField(Image, name='Images',related_name='Images_Offer',blank=True)
    
    tags = models.ManyToManyField(Tag, name='Tags',related_name='Tags_Offer',blank=True)

    suboffer = models.ManyToManyField(SubOffer,name='Suboffer',related_name='Suboffer_offer')
    
    def __str__(self):
        return f'{self.Offer_name}'

class BuyOffer(models.Model):
    
    buyer = models.ForeignKey(Buyer, name='Buyer', on_delete=models.CASCADE)
    
    offer = models.ForeignKey(Offer,name='Offer', on_delete=models.CASCADE)
    
    buy_date = models.DateTimeField(name='Buy_Date', auto_now=False, auto_now_add=True)
    
    amount = models.IntegerField(name='Amount',validators=(validate_positive,))
    
    def __str__(self):
        return f'{self.Buyer.MyUser.username} -> {self.Offer.Offer_name}; {self.Buy_Date}'
    
class Auction(models.Model):
    
    winner = models.OneToOneField(Buyer, name='Winner', on_delete=models.CASCADE, blank=True,null=True)
    
    offered = models.ForeignKey(Offer, name='Offered', on_delete=models.CASCADE)
    
    initial_date = models.DateTimeField(name='Initial_Date', auto_now=False, auto_now_add=False)
    
    duration = models.IntegerField(name='Duration_in_sec',validators=(validate_positive,))
    
    money_pool = models.IntegerField(name='Money',validators=(validate_positive,))
    
    def __str__(self):
        return f'{self.Offered.name} {self.Money}'