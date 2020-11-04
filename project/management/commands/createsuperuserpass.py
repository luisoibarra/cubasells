from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError
from django.utils import timezone

class Command(createsuperuser.Command):
    help = "Create superuser with password"
    
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            '--password', dest='password', default=None,
            help="Superuser's password"
        )
    
    def handle(self, *args, **options):
        password = options.get('password')
        username = options.get('username')
        database = options.get('database')
        
        if password and not username:
            raise CommandError("if password is given --username is required")
        
        super().handle(*args, **options)
        
        if password:
            user = self.UserModel._default_manager.db_manager(database).get(username=username)
            user.set_password(password)
            user.save()


