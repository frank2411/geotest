import os
from django.contrib.gis.utils import LayerMapping
from models import Circonscription

# Auto-generated `LayerMapping` dictionary for Circonscription model
circonscription_mapping = {
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


world_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'data', 'FED_CA_2_1_en.shp'))


def run(verbose=True):
    lm = LayerMapping(
        Circonscription, world_shp, circonscription_mapping,
        transform=True, encoding='utf-8')

    lm.save(strict=True, verbose=verbose)
