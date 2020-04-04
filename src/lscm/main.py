from urllib.request import urlopen
from flask import escape
from difflib import SequenceMatcher 
import pprint
pp = pprint.PrettyPrinter(indent=2)

def getStrip(fasta_id):
    url = 'https://www.uniprot.org/uniprot/' + fasta_id + '.fasta'
    response = urlopen(url)
    pid = response.readline()
    content = response.readlines()
    m = list(map(lambda b: b.rstrip().decode('utf-8'), content))
    return ''.join(m)

def getAllStrips(fasta_ids):
  strips = fasta_ids.split(",")
  allStrips = map(getStrip,strips)
  return allStrips

def findMatches(str1,str2):
  sm = SequenceMatcher(isjunk=None, a=str1, b=str2, autojunk=False)
  blocks = sm.get_matching_blocks()
  blocks.sort(key=lambda b: b.size, reverse=True)
  c = list(filter(lambda i: i != '', map(lambda blk: str1[blk.a:blk.a+blk.size], blocks)))
  return c

def getAllCandidates(fasta_ids, min_len = 4):
  minLen = 4
  strips = getAllStrips(fasta_ids)
  lstrips = list(strips)
  allCandidates = findMatches(lstrips[0], lstrips[1])
  for s in lstrips:
      allCandidates = list(filter(lambda c: (len(c) >= min_len and c in s), allCandidates))
  return allCandidates

def lscm(request):
    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    request_json = request.get_json(silent=True)
    fasta_ids = request_json['fasta_ids']
    ac = getAllCandidates(fasta_ids)
    retval = ','.join(ac)

    return (retval, 200, headers)
