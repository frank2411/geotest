from django.conf.urls import patterns, url
from terrains.views import *

urlpatterns = (
    url(r'^$', terrains, name='terrains'),
    url(r'^circonscriptions/$', circonscriptions, name='circonscriptions'),
)
