from nbt import nbt
import os
import AccountsClientPython

from django.db import models
from django.conf import settings

player_dir = getattr(settings, 'PLAYER_DIR', None)

class Player(models.Model):
    name = models.CharField(max_length=128)
    file_name = models.CharField(max_length=128)

    class Meta:
        app_label = 'minetourn'

    def __unicode__(self):
        return self.name

    @classmethod
    def scan(cls):
        """ Scan the player directory and add new players """
        if player_dir:
            player_data = {file_name: nbt.NBTFile(os.path.join(player_dir, file_name)) for file_name in
                           os.listdir(player_dir)}
            for file_name, data in player_data.items():
                try:
                    name = AccountsClientPython.profiles.find_profile_by_uuid(cls.get_uuid(file_name)).get('name')
                    cls.objects.get_or_create(name=name, file_name=file_name)
                except ValueError:
                    pass

    @classmethod
    def get_uuid(cls, file_name):
        """ Translate the filename into a UUID """
        return ''.join(file_name.split('.')[0].split('-'))

    @property
    def points(self):
        if not self.snapshot:
            self.create_snapshot()
        return self.snapshot.points

    @property
    def uuid(self):
        """ Cache the UUID and expose it """
        if not hasattr(self, '_uuid'):
            setattr(self, '_uuid', get_uuid(self.file_name))
        return self._uuid

    def create_snapshot(self):
        """ Create a current snapshot of the player's inventory """
        inv = nbt.NBTFile(os.path.join(player_dir, self.file_name)).get('Inventory')
        snapshot = Snapshot.objects.create(player=self)
        for inv_item in inv:
            try:
                item = Item.objects.get(name=inv_item.get('id'))
                if item:
                    InventoryItem.objects.create(name=inv_item.get('id'), count=inv_item.get('count'), snapshot=snapshot)
            except:
                pass

    @property
    def snapshot(self):
        """ Get most recent snapshot for this player """
        return self.snapshot_set.filter(player=self).last()

    @classmethod
    def create_snapshots(cls):
        for player in cls.objects.all():
            player.create_snapshot()

class Snapshot(models.Model):
    """ A snapshot of a players inventory at a moment in time """
    created_at = models.DateTimeField(auto_now_add=True)
    player = models.ForeignKey('Player')

    class Meta:
        app_label = 'minetourn'

    def __unicode__(self):
        return "Snapshot for %s @ %s" % (self.player, self.created_at)

    @property
    def points(self):
        return sum([item.value for item in self.inventory.all()])

    @property
    def inventory(self):
        return self.inventoryitem_set.all()

class Item(models.Model):
    """ Items that we want to assign value to """
    name = models.CharField(max_length=128)
    value = models.IntegerField()

    class Meta:
        app_label = 'minetourn'

    def __unicode__(self):
        return self.name

class InventoryItem(models.Model):
    """ Items in a players inventory """
    item = models.ForeignKey('Item')
    count = models.IntegerField()
    snapshot = models.ForeignKey('Snapshot')

    class Meta:
        app_label = 'minetourn'

    @property
    def value(self):
        return self.item.value * self.count

    def __unicode__(self):
        return '%s - %s' % (self.item, self.count)
