#!/usr/bin/python
# coding: utf-8 

# Get districts from wikimapia, generate lists of coordinates

import argparse, sys, pymapia
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


def createpoly(s, i):
    district = s.get_place_by_id(i)
    l = district['polygon']
    polyline = ""
    for dot in l:
        if polyline != "":
            polyline = polyline + ';'
        polyline = polyline + str(dot['y']) + "," + str(dot['x'])
    return polyline

parser = argparse.ArgumentParser(description='Takes Excel file and makes output in format specified')
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
			print createpoly(session, row[2].value)
		else:
			if currentcity == '':
				currentcity = row[0].value
				print row[0].value
				print row[1].value
				print createpoly(session, row[2].value)
			else:
				currentcity = row[0].value
				print ''
				print row[0].value
				print row[1].value
				print createpoly(session, row[2].value)
