import pytest
from .. import getAllCandidates
import pprint
pp = pprint.PrettyPrinter(indent=2)

def test_getAllCandidates():
    fasta_ids = "B5ZC00,P07204_TRBM_HUMAN"
    matches = getAllCandidates(fasta_ids)
    assert len(matches) == 2

def test_getAllCandidates_3chars():
    fasta_ids = "B5ZC00,P07204_TRBM_HUMAN"
    matches = getAllCandidates(fasta_ids,3)
    assert len(matches) == 6
