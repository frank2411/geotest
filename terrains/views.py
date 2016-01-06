import json
from django.shortcuts import render
from django.core import serializers
from terrains.forms import TerrainOrderingForm
from terrains.models import Terrain, Circonscription, MONTREAL_CIRCONSCRIPTIONS


allowed_orderings = [
    "-total_value",
    "-valeur_terrain",
    "-valeur_batiment",
    "total_value",
    "valeur_terrain",
    "valeur_batiment",
]


def home(request):
    return render(request, "terrains/home.html", {})


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

    return render(request, "terrains/home_terrains.html", context)


def circonscriptions(request):
    context = {}
    circonscriptions = Circonscription.objects.filter(
        fednum__in=MONTREAL_CIRCONSCRIPTIONS
    ).prefetch_related("terrains").distinct()
    terrains = Circonscription.get_circonscriptions_terrains(circonscriptions)

    context["circonscriptions_geojson"] = serializers.serialize(
        'geojson', circonscriptions)

    context["circonscriptions"] = circonscriptions
    context["terrains"] = terrains
    context["terrains_json"] = serializers.serialize("json", terrains)

    return render(request, "terrains/home_circonscriptions.html", context)
