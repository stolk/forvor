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
lneqs = [ ( float(x[0]), float(x[1]), float(x[2]), int(x[3]), int(x[4] ) ) for x in lneqs ]

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
	s0 = lneq[3]
	s1 = lneq[4]
	slope = -a / b
	print "<!-- a,b,c ", a,b,c, "slope", slope, "-->"
	v0 = verts[ e[1] ] if e[1] != -1 else None
	v1 = verts[ e[2] ] if e[2] != -1 else None
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
		assert len( candidates ) == 2
		cand0 = candidates[0]
		cand1 = candidates[1]
		pt = v0 if e[2] == -1 else v1
		cand0_largest_x = cand0[0] > cand1[0]
		if e[1] == -1 :
			cand0_largest_x = not cand0_largest_x
		if cand0_largest_x :
			v0 = pt
			v1 = cand0
		else:
			v1 = pt
			v0 = cand1
		if pt[0] < xlo or pt[0] > xhi or pt[1] < ylo or pt[1] > yhi :
			discard = True
	if not discard :
		print "  <path d=\"M %f %f L %f %f\" stroke=\"blue\" stroke-width=\"0.08\" />" % ( s*v0[0], s*v0[1], s*v1[0], s*v1[1] )

for p in pnts:
	print "  <path d=\"M %f %f L %f %f M %f %f L %f %f\" stroke=\"red\" stroke-width=\"0.04\" />" % ( s*p[0]-0.2,s*p[1], s*p[0]+0.2, s*p[1], s*p[0],s*p[1]-0.2, s*p[0],s*p[1]+0.2 )

print "</svg>"

