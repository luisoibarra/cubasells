from project.models import *
from project.buy.buy import OfferBuyer,bank,Bank

class AuctionBuyer(OfferBuyer):
    
    def __init__(self, offers, amounts, account, bank:Bank, password, deposit_account,price, *args, **kwargs):
        super().__init__(offers, amounts, account, bank, password, deposit_account)
        self._price = price
    
    def calculate_price(self):
        return self._price

class AuctionManager:
    
    def __init__(self, bank:Bank,buyer:AuctionBuyer):
        self.bank = bank
        self.buyer = buyer
    
    def on_time_range(self,auction:Auction):
        from django.utils import timezone
        now = timezone.now()
        return auction.Initial_Date <= now <= auction.Final_Date
    
    def can_book_auction(self,offered:Offer):
        qs = Offer.objects.none()
        qs |= Offer.objects.filter(id=offered.id)
        ob = self.buyer(qs,[1,],None,self.bank,None,None,None)
        if ob.check_products():
            ob.update_products()
            return ['Auction was saved']
        else:
            return ['Dont have the products needed to make the auction'] + ob.messages['error']
        
    def push(self,auction:Auction,push_bank_account:BankAccount,push_money,password):
        if not self.on_time_range(auction) or auction.Ended:
            return ['The auction is closed']
        if auction.Money < push_money:
            try:
                user = self.bank.get_account(push_bank_account.Account, password)
            except AssertionError as er:
                return [x for x in er.args]
                
            if user.Money >= push_money:
                auction.Winner = push_bank_account
                auction.Money = push_money
                auction.Password = password
                auction.save()
                return ['You pushed']
            else:
                return ['Dont have enough money to make the push']
        else:
            return ['The offered money is lower than the current price']
    
    def check_auctions(self):
        from datetime import timedelta
        from django.utils import timezone
        
        print("Check")
        auction_to_end = Auction.objects.filter(Final_Date__lte=timezone.now()).filter(Ended=False)
        
        
        for end in auction_to_end:
            self.end_auction(end)
    
    def end_auction(self,auction:Auction):
        if auction.Ended:
            return ['Auction already ended']
        
        winner = auction.Winner
        
        auction.Ended = True
        auction.save()
        
        if winner is None:
            qs = Offer.objects.none()
            qs |= Offer.objects.filter(id=auction.Offered.id)
            ob = self.buyer(qs,[1,],winner,self.bank,None,None,None)
            ob.update_products(True)
            return ['Nobody win the auction']
        try:
            user = self.bank.get_account(winner.Account,auction.Password)
        except AssertionError as er:
            return [x for x in er.args]
        

        if user.Money >= auction.Money:
            qs = Offer.objects.none()
            qs |= Offer.objects.filter(id=auction.Offered.id)
            ob = self.buyer(qs,[1,],winner,self.bank,auction.Password,auction.Deposit.Account,auction.Money)
            ob.update_products(True)
            ob.buy_offers()
            return ['Auction ended successfully']
        else:
            return ['Auction winner dont have enough money']
        
auction_manager = AuctionManager(bank,AuctionBuyer)   