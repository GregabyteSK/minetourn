from django.core.management.base import BaseCommand, CommandError
from ...models import Player

class Command(BaseCommand):
    help = 'Adds new players'

    def handle(self, *args, **options):
        Player.scan()