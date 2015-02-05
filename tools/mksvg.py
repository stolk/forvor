#!/usr/bin/python

import sys
import os

xlo = -1.0
xhi =  1.0
ylo = -1.0
yhi =  1.0

lines = sys.stdin.readlines()

verts = [ x.strip().split(' ')[1:] for x in lines if "v " in x ]
verts = [ ( float(x[0]), float(x[1]) ) for x in verts ]

edges = [ x.strip().split(' ')[1:] for x in lines if "e " in x ]
edges = [ ( int(x[0]), int(x[1]), int(x[2]) ) for x in edges ]

lneqs = [ x.strip().split(' ')[1:] for x in lines if "l " in x ]
lneqs = [ ( float(x[0]), float(x[1]), float(x[2]) ) for x in lneqs ]

pnts  = [ x.strip().split(' ')[1:] for x in lines if "s " in x ]
pnts  = [ ( float(x[0]), float(x[1]) ) for x in pnts ]

print\
'<?xml version="1.0" standalone="no"?>\n' \
'<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n' \
'<svg width="40pt" height="40pt" viewBox="-20 -20 40 40" xmlns="http://www.w3.org/2000/svg" version="1.1">\n'

s = 20.0

for e in edges:
	lneq = lneqs[ e[0] ]
	a = lneq[0]
	b = lneq[1]
	c = lneq[2]
	v0 = verts[ e[1] ]
	v1 = verts[ e[2] ]
	discard = False
	if -1 in e :
		candidates=[]
		y = ( c - a * xlo ) / b
		if y >= ylo and y <= yhi :
			candidates.append( (xlo,y) )
		y = ( c - a * xhi ) / b
		if y >= ylo and y <= yhi :
			candidates.append( (xhi,y) )
		x = ( c - b * ylo ) / a
		if x >= xlo and x <= yhi :
			candidates.append( (x,ylo) )
		x = ( c - b * yhi ) / a
		if x >= xlo and x <= xhi :
			candidates.append( (x,yhi) )
		v = v0 if e[2] == -1 else v1
		dsqr = [ ( (v[0]-cand[0])*(v[0]-cand[0]) + (v[1]-cand[1])*(v[1]-cand[1]), cand ) for cand in candidates ]
		if e[2] == -1 :
			v1 = min( dsqr )[ 1 ]
		else:
			v0 = min( dsqr )[ 1 ]
		if v[0] < xlo or v[0] > xhi or v[1] < ylo or v[1] > yhi :
			discard = True
	if not discard :
		print "  <path d=\"M %f %f L %f %f\" stroke=\"blue\" stroke-width=\"0.08\" />" % ( s*v0[0], s*v0[1], s*v1[0], s*v1[1] )

for p in pnts:
	print "  <path d=\"M %f %f L %f %f M %f %f L %f %f\" stroke=\"red\" stroke-width=\"0.04\" />" % ( s*p[0]-0.2,s*p[1], s*p[0]+0.2, s*p[1], s*p[0],s*p[1]-0.2, s*p[0],s*p[1]+0.2 )

print "</svg>"

