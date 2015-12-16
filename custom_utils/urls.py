from django.conf.urls import patterns, url
from custom_utils.views import *

urlpatterns = (
    url(r'^', home, name='home'),
)
