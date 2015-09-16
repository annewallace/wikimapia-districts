#!/usr/bin/python
# coding: utf-8 

# Get districts from wikimapia, merge them, generate lists of coordinates

import argparse, sys, pymapia

from shapely.geometry import Point, Polygon
from shapely.ops import unary_union, cascaded_union
from itertools import combinations

from codecs import getreader, getwriter
from openpyxl import load_workbook


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


def createpoly1(s, i):
    district = s.get_place_by_id(i)
    l = district['polygon']
    polylist = []
    for dot in l:
        polylist.append((float(dot['y']), float(dot['x'])))
    return polylist

# Takes list of polygons, merges them and does other things

def processpoly(polylist):
    print u"Полигоны"
    for p in polylist:
        pol = Polygon(p)
        print pol
    print u"Объединение"
    print cascaded_union([Polygon(p) for p in polylist])
    return 1

parser = argparse.ArgumentParser(description='Takes Excel file and makes output with merged polygons in format specified')
parser.add_argument('fname', metavar='FILE', type=str,
                   help='Excel file')

args = parser.parse_args()

session = pymapia.PyMapia("69911E52-1583C8FE-1C998725-04FC0632-4DB32EEE-50D8E7E4-713CE9D8-46BB4FDE")


wb = load_workbook(args.fname)
currentcity = ''
for sheet in wb:
    for row in sheet.rows:

        if currentcity == row[0].value:
            print row[1].value
            polylist = []
            for cell in row[2:]:
                if isinstance(cell.value, (int, long)):
                    polylist.append(createpoly1(session, cell.value))
            processpoly(polylist)
        else:
            if currentcity == '':
                currentcity = row[0].value
                print row[0].value
                print row[1].value
                polylist = []
                for cell in row[2:]:
                    if isinstance(cell.value, (int, long)):
                        polylist.append(createpoly1(session, cell.value))
                processpoly(polylist)
            else:
                currentcity = row[0].value
                print ''
                print row[0].value
                print row[1].value
                polylist = []
                for cell in row[2:]:
                    if isinstance(cell.value, (int, long)):
                        polylist.append(createpoly1(session, cell.value))
                processpoly(polylist)
