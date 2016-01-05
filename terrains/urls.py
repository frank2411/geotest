from django.conf.urls import url
from terrains.views import terrains, circonscriptions

urlpatterns = (
    url(r'^$', terrains, name='terrains'),
    url(r'^circonscriptions/$', circonscriptions, name='circonscriptions'),
)
