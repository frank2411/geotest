from django.shortcuts import render
from terrains.models import Terrain, Circonscription
from terrains.forms import CirconscriptionSearchForm
from django.core import serializers


def terrains(request):
    context = {}
    terrains = serializers.serialize("json", Terrain.objects.all())
    context["terrains"] = terrains

    return render(request, "home_terrains.html", context)


def circonscriptions(request):
    context = {}
    terrains = None
    # circonscriptions = Circonscription.objects.filter(provcode="QC")

    # context["to_polygon"] = serializers.serialize(
    #     "json", [circonscriptions[0]])
    # context["circonscriptions"] = circonscriptions

    if request.GET.get("circonscriptions"):
        terrains = Terrain.get_terrain_in_circonscription(
            request.GET.get("circonscriptions"))

    context["terrains"] = terrains
    context["form"] = CirconscriptionSearchForm(request.GET)
    return render(request, "circonscriptions.html", context)
