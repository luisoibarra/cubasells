from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
def validate_positive(number):
    if number < 0:
        raise ValidationError(f'{number} must be a positive number')


class Entity():
    
    name = models.CharField(name='Name',max_length=150)
    
    description = models.CharField(name="Description",max_length=400, null=True)
    
    create_date = models.DateTimeField(name="Create Date",auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.name
    

class RealEntity(Entity):
    
    email = models.EmailField(name='Email', max_length=254)
    
    phone = models.IntegerField(name='Phone number',null=True,validators=(validate_positive,))


class Product(models.Model,Entity):
    
    unit_price = models.FloatField(name='Price per unit',validators=(validate_positive,))
    
    amount = models.IntegerField(name = "Amount",validators=(validate_positive,))


class BankAccount(models.Model):
    
    bank_account = models.IntegerField(name='Bank account',validators=(validate_positive,))
    
    def __str__(self):
        return f'{self.bank_account}'
    

class User(models.Model, RealEntity):
    
    bank_accounts = models.ManyToManyField(BankAccount, name='User Bank Accounts')
    

class Store(models.Model,RealEntity):
    
    owner = models.ForeignKey(User, name='Owner', on_delete=models.CASCADE)   
    
    bank_account = models.ForeignKey(BankAccount,name = 'Bank account', on_delete=models.CASCADE) 
    
