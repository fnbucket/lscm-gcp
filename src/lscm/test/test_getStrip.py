import pytest
from .. import getStrip, getAllStrips
import pprint
pp = pprint.PrettyPrinter(indent=2)

def test_getStrip():
    id = "A2Z669"
    s = getStrip(id)
    assert len(s) > 0

def test_getAllStrips():
    ids = "B5ZC00,P07204_TRBM_HUMAN,P20840_SAG1_YEAST"
    s = getAllStrips(ids)
    assert(len(list(s)) == 3)

