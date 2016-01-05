import os
from django.test import TestCase
from django.core.files.base import ContentFile
from terrains.models import Terrain


class TerrainsTestCase(TestCase):

    def setUp(self):
        base_path = os.path.dirname(__file__)
        test_csv_dirname = "test_csv"
        test_csv_filename = "test.csv"
        self.csvfilepath = os.path.join(
            base_path, test_csv_dirname, test_csv_filename)
        csvfile = ContentFile(open(self.csvfilepath))
        # I simulate the filefield path attribute
        # only for test purposes
        csvfile.path = self.csvfilepath
        Terrain.generate_terrain_from_csv(csvfile)

    def test_terrains_count(self):
        self.assertEquals(Terrain.objects.all().count(), 14)

    def test_ranges_length(self):
        ranges = Terrain.generate_ranges(Terrain.objects.all(), None)
        self.assertEquals(len(ranges), 8)
