import pytest
from .. import findMatches
import pprint
pp = pprint.PrettyPrinter(indent=2)

def test_findMatches():
    str1 = "aaaaaaaabbbbbbbbgdgdgdgdgdnnnmmm"
    str2 = "cccccgdgdgdoonmmo"
    match1 = "gdgdgd"
    match2 = "nmm"
    matches = findMatches(str1, str2)
    
    assert len(matches) == 2
    assert match1 in matches
    assert match2 in matches

