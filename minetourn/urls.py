from django.conf.urls import url
from django.contrib import admin

import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.players, name='index'),
    url(r'^players/$', views.players, name='players'),
    url(r'^stats/$', views.stats, name='stats'),
]
