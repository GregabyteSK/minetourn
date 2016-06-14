from django.core.management.base import BaseCommand, CommandError
from ...models import Player

class Command(BaseCommand):
    help = 'Takes a snapshot of all users inventories'

    def handle(self, *args, **options):
        Player.create_snapshots()