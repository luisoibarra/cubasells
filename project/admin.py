from django.contrib import admin
from project.models import *
from project.bank.models import BankAccount as Bank
# Register your models here.

admin.site.register(Product)
admin.site.register(MyUser)
admin.site.register(Store)
admin.site.register(ShoppingCart)
admin.site.register(ShoppingOffer)
admin.site.register(Tag)
admin.site.register(Image)
admin.site.register(Offer)
admin.site.register(SubOffer)
admin.site.register(Auction)

# Confidential to admins
# admin.site.register(Chat)
# admin.site.register(BankAccount)
# admin.site.register(BuyOffer)

admin.site.register(Bank)