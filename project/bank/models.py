from django.db import models

# Create your models here.

class BankAccount(models.Model):

    name = models.CharField(name='Name',max_length=100)

    number = models.PositiveIntegerField(name='Number',unique=True)    

    password = models.CharField(name="Password", max_length=50)
    
    money = models.FloatField(name='Money')
    
    def __str__(self):
        return self.Name + f' {self.Number}: {self.Money}'
    