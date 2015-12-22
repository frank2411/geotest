from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
# from geopy.geocoders import GoogleV3
import csv
from django.contrib.gis.geos import GEOSGeometry


CAST_FIELDS = ["IntegerField", "FloatField"]
CAST_FUNCTIONS = {
    "IntegerField": int,
    "FloatField": float
}


class Circonscription(models.Model):
    nid = models.CharField(max_length=254)
    fednum = models.IntegerField()
    enname = models.CharField(max_length=100)
    frname = models.CharField(max_length=100)
    provcode = models.CharField(max_length=2)
    creadt = models.CharField(max_length=8)
    revdt = models.CharField(max_length=8)
    reporder = models.CharField(max_length=8)
    decpopcnt = models.IntegerField()
    quipopcnt = models.IntegerField()
    enlegaldsc = models.CharField(max_length=200)
    frlegaldsc = models.CharField(max_length=200)
    geom = models.PolygonField(srid=4326)
    objects = models.GeoManager()

    def __unicode__(self):
        return self.frname


class Terrain(models.Model):

    ID = models.IntegerField(_(u"Identifiant unique"), unique=True)
    munid = models.IntegerField(
        _(u"Identifiant unique municipalite"), null=True)
    arrid = models.CharField(
        _(u"Identifiant unique arrondissement"), max_length=5)

    civ = models.CharField(_(u"No civique de l'immeuble"), max_length=5)
    generique = models.CharField(_(u"Generique de rue"), max_length=15)
    specifique = models.CharField(_(u"Nom de la rue"), max_length=30)

    complet = models.CharField(_(u"CIV+GENERIQUE+SPECIFIQUE"), max_length=45)
    compte_foncier = models.CharField(
        _(u"Numero du compte foncier"), max_length=8)

    nom_proprietaire = models.CharField(
        _(u"Nom proprietaire de l'immeuble"), max_length=80)

    prenom_proprietaire = models.CharField(
        _(u"Prenom proprietaire de l'immeuble"),
        max_length=80, null=True, blank=True)

    complet_adr_prop = models.CharField(
        _(u"Adresse du proprietaire de l'immeuble"), max_length=100)

    ville_adr_prop = models.CharField(
        _(u"Ville Adresse proprietaire de l'immeuble"), max_length=45)

    cp_adr_prop = models.CharField(
        _(u"Code postal adresse proprietaire de l'immeuble"), max_length=6)

    valeur_batiment = models.IntegerField(
        _(u"Valeur du batiment selon le role d'evaluation fonciere 2013"))

    valeur_terrain = models.IntegerField(
        _(u"Valeur du terrain selon le role d'evaluation fonciere 2013"))

    regl_usage = models.CharField(
        _(u"Reglementation d'urbanisme 01-282 Ville-Marie"), max_length=10)

    regl_hauteur = models.FloatField(
        _(u"Hauteur (Reglementation d'urbanisme 01-282 Ville-Marie)"))

    regl_etages = models.CharField(
        _("Etages (Reglementation d'urbanisme 01-282 Ville-Marie)"),
        max_length=8)

    regl_densite = models.CharField(
        _(u"Densite (Reglementation d'urbanisme 01-282 Ville-Marie)"),
        max_length=8)

    regl_implantation = models.CharField(
        _(u"Implantation (Reglementation d'urbanisme 01-282 Ville-Marie)"),
        max_length=10)

    regl_unite_paysage = models.CharField(
        _(
            u"Unites de paysage "
            u"(Reglementation d'urbanisme 01-282 Ville-Marie)"),
        max_length=50)

    zone_patrimoine = models.CharField(
        _(
            u"Nom de l'immeuble patrimonial ou du site "
            u"patrimonial situe a proximite "
            u"selon la Loi sur le patrimoine culturel (Gouvernement du Quebec)"
        ),
        max_length=100)

    type_zone_patrimoine = models.CharField(
        _(
            u"Type de zone tampon autour de l'immeuble patrimonial"
            u"selon la Loi sur le patrimoine culturel (Gouvernement du Quebec)"
        ),
        max_length=30)

    interet_immeuble = models.CharField(
        _(u"Immeuble ayant un interet patrimonial"), max_length=5)

    interet_quartier = models.CharField(
        _(
            u"Quartier d'interet ou quartier cible"
            u" par l'arrondissement dans un PPU"),
        max_length=50)

    tampon_500_metro = models.CharField(
        _(u"Immeuble situe a moins de 500 m d'une station de metro"),
        max_length=3)

    description = models.CharField(
        _(u"Breve description du secteur"),
        max_length=254
    )

    total_value = models.IntegerField(null=True)

    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)

    coordinates = models.PointField(null=True, srid=4326)

    objects = models.GeoManager()

    @staticmethod
    def generate_ranges(queryset, ordering):
        ranges = {}
        ordering_attributes = {
            "-total_value": "total_value",
            "-valeur_terrain": "valeur_terrain",
            "-valeur_batiment": "valeur_batiment",
        }
        first_element = queryset.first()
        last_element = queryset.last()

        max_value = first_element.total_value
        min_value = last_element.total_value

        if ordering:
            max_value = getattr(first_element, ordering_attributes[ordering])
            min_value = getattr(last_element, ordering_attributes[ordering])

        # constant = max_value / 3
        constant = max_value / 5

        colors = {
            1: "red",
            2: "yellow",
            3: "blue",
            4: "azure",
            5: "green",
        }

        for i in reversed(range(1, 6)):
            if not ranges:
                ranges[i] = {
                    "min_value": min_value,
                    "max_value": constant,
                    "color": colors[i]
                }
                continue

            min_val = ranges[i + 1]["max_value"] + 1
            max_val = ranges[i + 1]["max_value"] + constant
            if i == 1:
                max_val = max_value
            ranges[i] = {
                "min_value": min_val,
                "max_value": max_val,
                "color": colors[i]
            }

        return ranges

    @staticmethod
    def get_terrain_in_circonscription(fednum):
        circonscription = Circonscription.objects.get(fednum=fednum)
        terrains = Terrain.objects.filter(
            coordinates__within=circonscription.geom)
        return terrains

    @staticmethod
    def clean_headers(headers):
        cleaned_headers = []
        headers.pop(0)

        for i, head in enumerate(headers):
            head = head.lower()
            head = head.rstrip('"')
            head = head.lstrip('"')
            # if i > 0:
            cleaned_headers.append(head)
        return cleaned_headers

    @staticmethod
    def generate_defaults(headers, row):
        row.pop(0)
        defaults = {}
        for i, head in enumerate(headers):
            value = row[i].rstrip('"')
            value = value.lstrip('"')
            field_type = Terrain._meta.get_field(
                head
            ).get_internal_type()

            # ENCODINGS FROM DEFAULT CSV ARE BROKEN
            # SO I IGNORE BROKEN CHARS
            defaults[head] = value.decode('ascii', 'ignore').encode("utf-8")
            if field_type in CAST_FIELDS:
                value = CAST_FUNCTIONS[field_type](value)
                defaults[head] = value

        return defaults

    @staticmethod
    def generate_terrain_from_csv(csvfile):
        csvfilebuffer = open(csvfile.path, 'rb')
        spamreader = csv.reader(csvfilebuffer, delimiter=',', quotechar='"')

        headers = spamreader.next()
        headers = Terrain.clean_headers(headers)

        for row in spamreader:
            to_check_id = int(row[0])
            defaults = Terrain.generate_defaults(
                headers, row)

            terrain, created = Terrain.objects.update_or_create(
                ID=to_check_id, defaults=defaults
            )

            if created:
                print "New object created"

        csvfilebuffer.close()

    def save(self, *args, **kwargs):
        pointstr = 'POINT({} {})'.format(self.longitude, self.latitude)
        self.coordinates = GEOSGeometry(pointstr, srid=4326)
        self.total_value = self.valeur_batiment + self.valeur_terrain
        super(Terrain, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.complet

    class Meta:
        verbose_name = _(u"Terrain")
        verbose_name_plural = _(u"Terrains")
        ordering = ["-total_value"]


class TerrainImport(models.Model):
    csvfile = models.FileField(upload_to="terrains")

    def __unicode__(self):
        return self.csvfile.name.encode("utf-8")

    class Meta:
        verbose_name = _(u"Terrain import")
        verbose_name_plural = _(u"Terrain imports")
