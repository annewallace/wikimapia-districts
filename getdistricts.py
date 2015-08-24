#!/usr/bin/python
# coding: utf-8 

# Get districts from wikimapia, generate lists of coordinates

import sys
import pymapia
from codecs import getreader, getwriter


sys.stdin = getreader('utf-8')(sys.stdin)
sys.stdout = getwriter('utf-8')(sys.stdout)

def dumpclean(obj):
    if type(obj) == dict:
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print k
                dumpclean(v)
            else:
                print '%s : %s' % (k, v)
    elif type(obj) == list:
        for v in obj:
            if hasattr(v, '__iter__'):
                dumpclean(v)
            else:
                print v
    else:
        print obj

session = pymapia.PyMapia("69911E52-1583C8FE-1C998725-04FC0632-4DB32EEE-50D8E7E4-713CE9D8-46BB4FDE")
o = session.get_place_by_id(9762956)

print o['title']
print dumpclean(o)
