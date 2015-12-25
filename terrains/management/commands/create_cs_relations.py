from django.core.management.base import BaseCommand, CommandError
from terrains.models import Terrain, Circonscription
from django.db.models import Avg, Max, Min


class Command(BaseCommand):
    help = 'Create relations between the terrains and the circonscriptions'

    def handle(self, *args, **options):
        terrains = Terrain.objects.all()

        for terrain in terrains:
            circonscription = Circonscription.objects.get(
                geom__contains=terrain.coordinates, provcode="QC")
            circonscription.terrains.add(terrain)

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
