from user.models import MyUser
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Delete users'

    def add_arguments(self, parser):
        parser.add_argument('user_id', nargs='+', type=int, help='User ID')

    def handle(self, *args, **kwargs):
        users_ids = kwargs['user_id']

        for user_id in users_ids:
            try:
                user = MyUser.objects.get(pk=user_id)
                user.delete()
                self.stdout.write(self.style.SUCCESS('User "%s (%s)" deleted with success!' % (user.phone_number, user_id)))
            except MyUser.DoesNotExist:
                self.stdout.write(self.style.WARNING('User with id "%s" does not exist.' % user_id))