from django.contrib import admin
from django.contrib.gis import admin as geoadmin
from terrains.models import Terrain, TerrainImport, Circonscription
from terrains.forms import TerrainImportAdminForm


class TerrainAdmin(geoadmin.GeoModelAdmin):
    pass


class TerrainImportAdmin(admin.ModelAdmin):
    form = TerrainImportAdminForm

    def save_model(self, request, obj, form, change):
        obj.save()
        Terrain.generate_terrain_from_csv(obj.csvfile)


class CirconscriptionAdmin(admin.ModelAdmin):
    search_fields = ("enname", "frname", )
    list_filter = ("provcode", )


admin.site.register(Terrain, TerrainAdmin)
admin.site.register(TerrainImport, TerrainImportAdmin)
admin.site.register(Circonscription, CirconscriptionAdmin)
