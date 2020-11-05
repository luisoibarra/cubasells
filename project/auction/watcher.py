from multiprocessing import Process
from project.auction.manager import AuctionManager, auction_manager
import Cubasells.settings as settings
import time

class AuctionWatcher:
    def __init__(self, auction_manager:AuctionManager, interval:float, func=None):
        self.interval = interval
        if func is None:
            def watcher():
                while True:
                    auction_manager.check_auctions()
                    time.sleep(self.interval)     
            self.auction_watcher_func = watcher
        else:
            self.auction_watcher_func = func
            
    def start_watcher(self):
        print("AuctionWatcher started")
        self.process = Process(target=self.auction_watcher_func)
        self.process.start()
    
    def is_watching(self):
        return self.process.is_alive()
    
    def end_watcher(self):
        self.process.terminate()

if settings.AUCTION_TIMER:
    auction_watcher = AuctionWatcher(auction_manager,settings.AUCTION_TIMER)
    auction_watcher.start_watcher()