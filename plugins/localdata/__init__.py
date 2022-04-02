from pelican import signals
from . import generators


def get_generators(pelican_object):
    return generators.JsonDataGenerator

def register():
    signals.get_generators.connect(get_generators)