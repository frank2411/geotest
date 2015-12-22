from django.shortcuts import render
from terrains.models import Terrain, Circonscription
from terrains.forms import CirconscriptionSearchForm, TerrainOrderingForm
from django.core import serializers
import json

allowed_orderings = [
    "-total_value",
    "-valeur_terrain",
    "-valeur_batiment",
    "total_value",
    "valeur_terrain",
    "valeur_batiment",
]


def terrains(request):
    context = {}
    ordering_param = None
    ordering_form = TerrainOrderingForm()

    terrains = Terrain.objects.all()
    ordering = request.GET.get("ordering")

    if ordering and ordering in allowed_orderings:
        ordering_form = TerrainOrderingForm(request.GET)
        ordering_param = ordering
        terrains = terrains.order_by(ordering)

    terrains_json = serializers.serialize("json", terrains)
    ranges = Terrain.generate_ranges(terrains, ordering)

    context["ranges"] = ranges
    context["ranges_json"] = json.dumps(ranges)
    context["terrains_json"] = terrains_json
    context["terrains"] = terrains
    context["ordering_form"] = ordering_form
    context["ordering_param"] = ordering_param

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
