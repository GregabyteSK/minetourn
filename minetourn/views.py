import models
import json
import datetime
import itertools

from django.shortcuts import get_object_or_404, render
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings

def stats(request):
    snapshots = models.Snapshot.objects.all()
    if hasattr(settings, 'SHORT_DISPLAY'):
        now = datetime.datetime.now()
        then = now - datetime.timedelta(hours=1)
        snapshots = snapshots.filter(created_at__range=(then, now))
    data = []
    players = json.dumps(list(models.Player.objects.all().values_list('name', flat=True)))

    def date_hour(timestamp):
        return timestamp.strftime("%x %H:%M")

    groups = itertools.groupby(snapshots, lambda x: date_hour(x.created_at))

    for group, matches in groups:
        data.append(dict({'time':group }, **{match.player.name:match.points for match in matches}))
    data = json.dumps(data, cls=DjangoJSONEncoder)
    return render(request, template_name='templates/stats.html', context=locals())

def players(request, id=None):
    players = models.Player.objects.all()
    return render(request, template_name='templates/players.html', context=locals())