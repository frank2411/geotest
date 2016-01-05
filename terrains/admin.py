from django.contrib import admin
from django.contrib.gis import admin as geoadmin
from terrains.models import Terrain, TerrainImport, Circonscription
from terrains.forms import TerrainImportAdminForm


class TerrainAdmin(geoadmin.OSMGeoAdmin):
    list_display = (
        "complet",
        "nom_proprietaire",
        "prenom_proprietaire",
    )


class TerrainImportAdmin(admin.ModelAdmin):
    form = TerrainImportAdminForm

    def save_model(self, request, obj, form, change):
        obj.save()
        Terrain.generate_terrain_from_csv(obj.csvfile)


class CirconscriptionAdmin(geoadmin.OSMGeoAdmin):
    search_fields = ("enname", "frname", )
    list_filter = ("provcode", )
    list_display = (
        "frname",
        "fednum",
        "provcode",
        "valeur_terrain_moyen",
        "valeur_batiment_moyen",
        "valeur_terrain_min",
        "valeur_batiment_min",
        "valeur_terrain_max",
        "valeur_batiment_max",
    )
    list_display_links = ("frname", "fednum", "provcode")


admin.site.register(Terrain, TerrainAdmin)
admin.site.register(TerrainImport, TerrainImportAdmin)
admin.site.register(Circonscription, CirconscriptionAdmin)
