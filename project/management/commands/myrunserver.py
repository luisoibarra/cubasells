from django.core.management.commands import runserver
import Cubasells.settings as settings

class Command(runserver.Command):
    
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            '--watcher', dest='watcher', default=0, type=int,
            help="The interval of checking the auctions. If not given the auctions will not be checked"
        )
        
    
    def handle(self, *args, **options):
        watcher = options.get('watcher')
        if watcher:
            settings.AUCTION_TIMER = watcher
        super().handle(*args, **options)

