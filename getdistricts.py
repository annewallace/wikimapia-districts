#!/usr/bin/python
# coding: utf-8 

# Get districts from wikimapia, generate lists of coordinates

import argparse, sys, pymapia
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

def print_test(o):
	return 0

def print_lines(o):
	return 0


parser = argparse.ArgumentParser(description='Retrives polygons from wikimapia')
parser.add_argument('ids', metavar='ID', type=int, nargs='+',
                   help='IDs of object to retrive')
parser.add_argument('-t', dest='testformat', action='store_true',
                   help='print coords for testing in yandex api (default: print lists of coords in specified output format)')

args = parser.parse_args()

session = pymapia.PyMapia("69911E52-1583C8FE-1C998725-04FC0632-4DB32EEE-50D8E7E4-713CE9D8-46BB4FDE")

plist = []
for i in args.ids:
	district = session.get_place_by_id(i)
	plist.append(district['polygon'])

if args.testformat :
	print "["
	for l in plist:
		print "[["
		for dot in l:
			print "[" + str(dot['y']) + "," + str(dot['x']) + "],"
		print "]],"
	print "];"

else:
	for l in plist:
		polyline = ""
		for dot in l:
			if polyline != "":
				polyline = polyline + ';'
			polyline = polyline + str(dot['y']) + "," + str(dot['x'])

	print polyline
