from django.core.management.base import BaseCommand, CommandError
from terrains.models import Terrain, Circonscription, MONTREAL_CIRCONSCRIPTIONS
from django.db.models import Avg, Max, Min


class Command(BaseCommand):
    help = 'Create relations between the terrains and the circonscriptions'

    # MONTREAL_CIRCONSCRIPTIONS = [
    #     u"Ahuntsic-Cartierville",
    #     u"Bourassa",
    #     u"Hochelaga",
    #     u"Honor\u00e9-Mercier",
    #     u"LaSalle--\u00c9mard--Verdun",
    #     u"Lac-Saint-Louis",
    #     u"La Pointe-de-l'\u00cele",
    #     u"Dorval--Lachine--LaSalle",
    #     u"Laurier--Sainte-Marie",
    #     u"Mont-Royal",
    #     u"Notre-Dame-de-Gr\u00e2ce--Westmount",
    #     u"Outremont",
    #     u"Papineau",
    #     u"Pierrefonds--Dollard",
    #     u"Rosemont--La Petite-Patrie",
    #     u"Saint-Laurent",
    #     u"Saint-L\u00e9onard--Saint-Michel",
    #     u"Ville-Marie--Le Sud-Ouest--\u00cele-des-Soeurs",
    # ]

    def handle(self, *args, **options):
        terrains = Terrain.objects.all()

        for terrain in terrains:
            try:
                circonscription = Circonscription.objects.get(
                    geom__contains=terrain.coordinates,
                    fednum__in=MONTREAL_CIRCONSCRIPTIONS)
            except Circonscription.DoesNotExist:
                print "TERRAIN IS OUT OF MONTREAL"
                continue

            circonscription.terrains.add(terrain)
            print "TERRAIN ASSOCIATED"

        circonscriptions = Circonscription.objects.filter(
            terrains__isnull=False).distinct().annotate(
            avg_valeur_batiment=Avg("terrains__valeur_batiment"),
            avg_valeur_terrain=Avg("terrains__valeur_terrain"),
            max_valeur_batiment=Max("terrains__valeur_batiment"),
            max_valeur_terrain=Max("terrains__valeur_terrain"),
            min_valeur_batiment=Min("terrains__valeur_batiment"),
            min_valeur_terrain=Min("terrains__valeur_terrain")
        )

        for circonscription in circonscriptions:
            print "Circonscription ", circonscription
            print "Terrains count ", circonscription.terrains.count()
            circonscription.valeur_terrain_moyen = (
                circonscription.avg_valeur_terrain)
            circonscription.valeur_batiment_moyen = (
                circonscription.avg_valeur_batiment)
            circonscription.valeur_terrain_min = (
                circonscription.min_valeur_terrain)
            circonscription.valeur_batiment_min = (
                circonscription.min_valeur_batiment)
            circonscription.valeur_terrain_max = (
                circonscription.max_valeur_terrain)
            circonscription.valeur_batiment_max = (
                circonscription.max_valeur_batiment)

            circonscription.save()

        print "SCRIPT ENDED WITH NO ERRORS"
