import os
from django.contrib.gis.utils import LayerMapping
from terrains.models import Circonscription

# Auto-generated `LayerMapping` dictionary for Circonscription model
CIRCONSCRIPTION_MAPPING = {
    'nid': 'NID',
    'fednum': 'FEDNUM',
    'enname': 'ENNAME',
    'frname': 'FRNAME',
    'provcode': 'PROVCODE',
    'creadt': 'CREADT',
    'revdt': 'REVDT',
    'reporder': 'REPORDER',
    'decpopcnt': 'DECPOPCNT',
    'quipopcnt': 'QUIPOPCNT',
    'enlegaldsc': 'ENLEGALDSC',
    'frlegaldsc': 'FRLEGALDSC',
    'geom': 'POLYGON',
}


WORLD_SHP = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'data', 'FED_CA_2_1_en.shp'))


def run(verbose=True):
    lm = LayerMapping(
        Circonscription, WORLD_SHP, CIRCONSCRIPTION_MAPPING, encoding='utf-8')

    lm.save(strict=True, verbose=verbose)
