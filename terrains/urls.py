from django.conf.urls import url
from terrains.views import terrains, circonscriptions, home

urlpatterns = (
    url(r'^$', home, name='home'),
    url(r'^terrains/$', terrains, name='terrains'),
    url(r'^circonscriptions/$', circonscriptions, name='circonscriptions'),
)
