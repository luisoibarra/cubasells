from django.core.management.commands import runserver
from project.auction.watcher import auction_watcher

class Command(runserver.Command):
    
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            '--watcher', dest='watcher', default=0,
            help="The interval of checking the auctions. If not given the auctions will not be checked"
        )
        
    
    def handle(self, *args, **options):
        watcher = options.get('watcher')
        super().handle(*args, **options)
        if watcher:
            auction_watcher.interval = watcher
            auction_watcher.start_watcher()

