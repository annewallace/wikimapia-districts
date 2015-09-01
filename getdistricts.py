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
                   help='make html code to test with yandex api (default: print lists of coords in specified output format)')

args = parser.parse_args()

session = pymapia.PyMapia("69911E52-1583C8FE-1C998725-04FC0632-4DB32EEE-50D8E7E4-713CE9D8-46BB4FDE")

plist = []
for i in args.ids:
	district = session.get_place_by_id(i)
	plist.append(district['polygon'])

if args.testformat :
    # Calculate center
    sumx = 0.0
    sumy = 0.0
    midx = 0.0
    midy = 0.0
    count = 0
    for l in plist:
        for dot in l:
            sumy = sumy + dot['y']
            sumx = sumx + dot['x']
            count = count + 1
    midx = sumx/count
    midy = sumy/count
    print u"""<!DOCTYPE html>
<html>
<head>
    <title>Границы районов - API Яндекс.Карт v 2.x</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <script src="http://api-maps.yandex.ru/2.0/?load=package.full&lang=ru-RU"
            type="text/javascript"></script>
    <script type="text/javascript">
        // Как только будет загружен API и готов DOM, выполняем инициализацию
        ymaps.ready(init);
 
        function init () {
            var myMap = new ymaps.Map("map", {"""

    print "center: [" + str(midy) + "," + str(midx) + "],"

    print u"""
                    zoom: 10
                });
            var coords =

	"""
    print "["
    for l in plist:
		print "[["
		for dot in l:
			print "[" + str(dot['y']) + "," + str(dot['x']) + "],"
		print "]],"
    print "];"

    print u"""
            // Создаем многоугольник
                for (i = 0; i < coords.length; i++) {            
                    myPolygon = new ymaps.Polygon(coords[i]);
                    myMap.geoObjects.add(myPolygon);
                }
            }
    </script>
</head>
 
<body>
<h2>Карта с полигонами</h2>
 
<div id="map" style="width:800px; height:600px"></div>
</body>
 
</html>"""

else:
    for l in plist:
        polyline = ""
        for dot in l:
            if polyline != "":
                polyline = polyline + ';'
            polyline = polyline + str(dot['y']) + "," + str(dot['x'])
        print polyline
