from django.contrib import admin
import models

for model in [models.Player, models.InventoryItem, models.Item, models.Snapshot]:
    admin.site.register(model)
