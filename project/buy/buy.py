from project.models import *
from django.db.models.query import QuerySet
from project.bank.models import BankAccount as MyBank

class Bank:
    
    accounts = None # List of BankAccounts
    
    def __init__(self, accounts = [], *args, **kwargs):
        self.accounts = MyBank
    
    def __get_user(self,number)->MyBank:
        user_account = [ ac for ac in self.accounts.objects.filter(Number = number) ]
        if len(user_account) == 1:
            return user_account[0]
        else:
            assert False, 'No accounts number match with number'
    
    def add_account(self,name,number,password,money=0):
        acc = self.accounts(name,number,password,money)
        acc.save()
    
    def get_account(self,number,password)->MyBank:
        user_account = self.__get_user(number)
        assert user_account.Password == password, 'Wrong Password'
        return user_account
    
    def insert_money(self, number, money):
        user_account = self.__get_user(number)
        assert money > 0, 'the money to insert must be a positive number'
        self.accounts.objects.filter(id=user_account.id).update(Money=user_account.Money+money)
        
    def remove_money(self, number, money, password):
        assert money > 0, 'the money to remove must be a positive number'
        user_account = self.get_account(number,password)
        assert user_account.Money >= money, 'Dont have enough money to remove'
        self.accounts.objects.filter(id=user_account.id).update(Money=user_account.Money-money)

class OfferBuyer:
    
    def __init__(self, offers, amounts, account, bank:Bank, password, deposit_account, *args, **kwargs):
        self.account = account
        self.amounts = amounts
        self.bank = bank
        self.password = password
        self.offers = offers
        self.messages = dict()
        self.deposit_account = deposit_account
        self._products_to_buy_amount = None
        self._products = None
        self._price = None
        
    def calculate_price(self):
        """
        Calculates the price of the offers with the amounts
        """
        if self._price is None:
            price = 0
            for i,offer in enumerate(self.offers):
                price += offer.Price*self.amounts[i]
            self._price = price
        return self._price
        
    def check_price(self):
        price = self.calculate_price()
        try:
            bank_account = self.bank.get_account(self.account.Account,self.password)
        except AssertionError as err:
            self.report_error('\n'.join(err.args))
            return False
        money = bank_account.Money
        if price > money:
            self.report_error(f'Not enough money to make operation, money:{money} < price:{price}')
            return False
        return True
    
    def get_products(self):
        if self._products is None:
            product_to_buy = self.get_to_buy_amount()
            self._products = Product.objects.all().filter(id__in=product_to_buy)
        return self._products
    
    def get_to_buy_amount(self):
        """
        returns a dictionary of id product to amount to buy of that product
        """
        if self._products_to_buy_amount is None:
            product_to_buy = {}
            for i,off in  enumerate(self.offers):
                for sub in off.Suboffer.all():
                    prod = sub.Product_offer
                    amount = product_to_buy.get(prod.id,0)
                    amount += sub.Amount * self.amounts[i]
                    product_to_buy[prod.id] = amount
            self._products_to_buy_amount = product_to_buy
        return self._products_to_buy_amount
        
    def check_products(self):
        product_to_buy = self.get_to_buy_amount()

        products = self.get_products()
        
        not_enough_products = [prod for prod in products if prod.Store_Amount < product_to_buy[prod.id] ]
        
        if not_enough_products:
            for prod in not_enough_products:
                self.report_error(f'Product {prod.Name} dont have enough items stored to make the sale. Wanted: {product_to_buy[prod.id]} Stored: {prod.Store_Amount}')
            return False
        else:
            return True
    
    def update_products(self,add_products = False):
        id_products = self.get_to_buy_amount()
        for prod in self.get_products():
            if add_products:
                Product.objects.filter(id=prod.id).update(Store_Amount = prod.Store_Amount+id_products[prod.id])
            else:
                Product.objects.filter(id=prod.id).update(Store_Amount = prod.Store_Amount-id_products[prod.id])
    
    def buy_offers(self):
        self.clean_messages()
        try:
            account = self.bank.get_account(self.account.Account,self.password)
        except AssertionError as err:
            self.report_error(err.args[0])
            return self.messages
            
        if self.check_products() and self.check_price():
            self.update_products()
            for i,offer in enumerate(self.offers):
                buyed = BuyOffer(Buyer=self.account,Offer=offer,Amount=self.amounts[i])
                buyed.save()
            self.bank.remove_money(self.account.Account,self.calculate_price(),self.password)
            self.bank.insert_money(self.deposit_account,self.calculate_price())
            self.messages['success'] = ['Operation Successful',f'You have ${account.Money} left']
        return self.messages
    
    def clean_messages(self):
        self.messages.clear()
                
    def report_error(self,error):
        errors = self.messages.get('error',[])    
        errors.append(error)
        self.messages['error'] = errors   

bank = Bank()
 
def buy_offers(account:BankAccount,password:str,shopping_offers:QuerySet)->dict:
    global_message = {}
    for shop_id in set(x['Offer__Store__id'] for x in shopping_offers.values('Offer__Store__id')):
        shop_offers = shopping_offers.filter(Offer__Store__id=shop_id)
        offers = Offer.objects.none()
        amounts = []
        for i,shop_off in enumerate(shop_offers):
            amounts.append(shop_off.Amount)
            offers |= Offer.objects.filter(id=shop_off.Offer.id)
        buyer = OfferBuyer(offers,amounts,account,bank,password,offers.first().Store.Bank_Account.Account)
        message = buyer.buy_offers()
        for x in message:
            if x in global_message:
                global_message[x].extend(message[x])
            else:
                global_message[x] = message[x]
    return global_message

