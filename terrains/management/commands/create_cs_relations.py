from django.core.management.base import BaseCommand, CommandError
from terrains.models import Terrain, Circonscription
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

    # List of fednum for montreal circonscriptions
    MONTREAL_CIRCONSCRIPTIONS = [
        24003,
        # u"Ahuntsic-Cartierville",
        24015,
        # u"Bourassa",
        24028,
        # u"Hochelaga",
        24029,
        # u"Honor\u00e9-Mercier",
        24037,
        # u"LaSalle--\u00c9mard--Verdun",
        24036,
        # u"Lac-Saint-Louis",
        24033,
        # u"La Pointe-de-l'\u00cele",
        24024,
        # u"Dorval--Lachine--LaSalle",
        24039,
        # u"Laurier--Sainte-Marie",
        24052,
        # u"Mont-Royal",
        24053,
        # u"Notre-Dame-de-Gr\u00e2ce--Westmount",
        24054,
        # u"Outremont",
        24055,
        # u"Papineau",
        24056,
        # u"Pierrefonds--Dollard",
        24064,
        # u"Rosemont--La Petite-Patrie",
        24068,
        # u"Saint-Laurent"
        24069,
        # u"Saint-L\u00e9onard--Saint-Michel"
        24077,
        # u"Ville-Marie--Le Sud-Ouest--\u00cele-des-Soeurs"
    ]

    def handle(self, *args, **options):
        terrains = Terrain.objects.all()

        for terrain in terrains:
            try:
                circonscription = Circonscription.objects.get(
                    geom__contains=terrain.coordinates,
                    fednum__in=self.MONTREAL_CIRCONSCRIPTIONS)
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
