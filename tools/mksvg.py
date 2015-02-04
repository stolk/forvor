#!/usr/bin/python

import sys
import os

lines = sys.stdin.readlines()

verts = [ x.strip().split(' ')[1:] for x in lines if "v " in x ]
verts = [ ( 20*float(x[0]), 20*float(x[1]) ) for x in verts ]

edges = [ x.strip().split(' ')[2:] for x in lines if "e " in x ]
edges = [ ( int(x[0]), int(x[1]) ) for x in edges ]

pnts  = [ x.strip().split(' ')[1:] for x in lines if "s " in x ]
pnts  = [ ( 20*float(x[0]), 20*float(x[1]) ) for x in pnts ]

print\
'<?xml version="1.0" standalone="no"?>\n' \
'<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n' \
'<svg width="40pt" height="40pt" viewBox="-20 -20 40 40" xmlns="http://www.w3.org/2000/svg" version="1.1">\n'

for e in edges:
	v0 = verts[ e[0] ]
	v1 = verts[ e[1] ]
	if ( not -1 in e ) :
		print "  <path d=\"M %f %f L %f %f\" stroke=\"blue\" stroke-width=\"0.05\" />" % ( v0[0], v0[1], v1[0], v1[1] )

for p in pnts:
	print "  <path d=\"M %f %f L %f %f M %f %f L %f %f\" stroke=\"red\" stroke-width=\"0.02\" />" % ( p[0]-0.12, p[1], p[0]+0.12, p[1], p[0],p[1]-0.12, p[0],p[1]+0.12 )

print "</svg>"

