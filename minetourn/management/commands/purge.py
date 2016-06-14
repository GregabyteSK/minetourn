from django.core.management.base import BaseCommand, CommandError

from minetourn import models

class Command(BaseCommand):
    help = 'Clears the server for a new game'

    def handle(self, *args, **options):
        for model in [models.Player, models.Snapshot, models.InventoryItem]:
            model.objects.all().delete()