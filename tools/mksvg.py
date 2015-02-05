#!/usr/bin/python

import sys
import os

xlo = -1.0
xhi =  1.0
ylo = -1.0
yhi =  1.0

"""
clip_edges

Does a few things to clean up edges:
Edges that go to infinity are clipped.
Edges that go outside clipping area are clipped.
Edges that have both end points outside the clipping rectangle are discarded.

Returns a new list of edges.
"""
def clip_edges( verts, edges, lneqs, pnts ) :
	newvertidx = len(verts)
	accepted_edges = []
	for eidx, e in enumerate(edges):
		lneq = lneqs[ e[0] ]
		a = lneq[0]
		b = lneq[1]
		c = lneq[2]
		s0 = lneq[3]
		s1 = lneq[4]
		v0 = verts[ e[1] ] if e[1] != -1 else None
		v1 = verts[ e[2] ] if e[2] != -1 else None
		v0oob = v0 and ( v0[0] < xlo or v0[0] > xhi or v0[1] < ylo or v0[1] > yhi )
		v1oob = v1 and ( v1[0] < xlo or v1[0] > xhi or v1[1] < ylo or v1[1] > yhi )
		if -1 in e :
			known = 2 if e[1] == -1 else 1
			unkno = 1 if e[1] == -1 else 2
			pt = v0 if unkno == 2 else v1
			if pt[0] >= xlo and pt[0] <= xhi and pt[1] >= ylo and pt[1] <= yhi :
				candidates=[]
				y = ( c - a * xlo ) / b
				if y >= ylo and y <= yhi :
					candidates.append( (xlo,y) )
				y = ( c - a * xhi ) / b
				if y >= ylo and y <= yhi :
					candidates.append( (xhi,y) )
				x = ( c - b * ylo ) / a
				if x >= xlo and x <= xhi :
					candidates.append( (x,ylo) )
				x = ( c - b * yhi ) / a
				if x >= xlo and x <= xhi :
					candidates.append( (x,yhi) )
				assert len( candidates ) == 2
				cand0 = candidates[0]
				cand1 = candidates[1]
				cand0_largest_x = cand0[0] > cand1[0]
				if unkno == 1 :
					cand0_largest_x = not cand0_largest_x
				if cand0_largest_x :
					v0 = pt
					v1 = cand0
					verts.append( cand0 )
				else:
					v1 = pt
					v0 = cand1
					verts.append( cand1 )
				newe = ( e[0], e[1], newvertidx ) if unkno == 2 else ( e[0], newvertidx, e[2] )
				#edges[ eidx ] = newe
				newvertidx += 1
				accepted_edges.append( newe )

		elif v0oob and v1oob :
			pass

		elif not v0oob and not v1oob :
			accepted_edges.append( e )

		elif v0oob :
			newv = None
			if v0[0] < xlo:
				y = ( c - a * xlo ) / b
				if y >= ylo and y <= yhi :
					newv = (xlo,y)
			if v0[0] > xhi :
				y = ( c - a * xhi ) / b
				if y >= ylo and y <= yhi :
					newv = (xhi,y)
			if v0[1] < ylo:
				x = ( c - b * ylo ) / a
				if x >= xlo and x <= xhi :
					newv = (x,ylo)
			if v0[1] > yhi:
				x = ( c - b * yhi ) / a
				if x >= xlo and x <= xhi :
					newv = (x,yhi)
			assert newv
			verts.append( newv )
			newe = ( e[0], newvertidx, e[2] )
			newvertidx += 1
			accepted_edges.append( newe )

		elif v1oob :
			newv = None
			if v1[0] < xlo:
				y = ( c - a * xlo ) / b
				if y >= ylo and y <= yhi :
					newv = (xlo,y)
			if v1[0] > xhi :
				y = ( c - a * xhi ) / b
				if y >= ylo and y <= yhi :
					newv = (xhi,y)
			if v1[1] < ylo:
				x = ( c - b * ylo ) / a
				if x >= xlo and x <= xhi :
					newv = (x,ylo)
			if v1[1] > yhi:
				x = ( c - b * yhi ) / a
				if x >= xlo and x <= xhi :
					newv = (x,yhi)
			assert newv
			verts.append( newv )
			newe = ( e[0], e[1], newvertidx )
			newvertidx += 1
			accepted_edges.append( newe )

	return accepted_edges


def add_border_edges( verts, edges ) :
	newvertidx = len( verts )

	btle_idx = newvertidx
	verts.append( ( xlo, ylo ) )
	newvertidx += 1

	btri_idx = newvertidx
	verts.append( ( xhi, ylo ) )
	newvertidx += 1

	tple_idx = newvertidx
	verts.append( ( xlo, yhi ) )
	newvertidx += 1

	tpri_idx = newvertidx
	verts.append( ( xhi, yhi ) )
	newvertidx += 1

	le = []
	ri = []
	tp = []
	bt = []

	for vidx, v in enumerate(verts) :
		if v[0] == xlo :
			le.append( ( v[1], v, vidx ) )
		if v[0] == xhi :
			ri.append( ( v[1], v, vidx ) )
		if v[1] == ylo :
			bt.append( ( v[0], v, vidx ) )
		if v[1] == yhi :
			tp.append( ( v[0], v, vidx ) )

	le.sort()
	ri.sort()
	tp.sort()
	bt.sort()

	for i in range( len(le) - 1 ) :
		newe = ( -1, le[i+0][2], le[i+1][2] )
		edges.append( newe )

	for i in range( len(ri) - 1 ) :
		newe = ( -1, ri[i+0][2], ri[i+1][2] )
		edges.append( newe )

	for i in range( len(bt) - 1 ) :
		newe = ( -1, bt[i+0][2], bt[i+1][2] )
		edges.append( newe )

	for i in range( len(tp) - 1 ) :
		newe = ( -1, tp[i+0][2], tp[i+1][2] )
		edges.append( newe )


def assemble_polygons( verts, edges, lneqs, pnts ) :

	numsites = len( pnts )
	site_edges = [ [] for x in range( numsites ) ]

	for e in edges :
		lneq = lneqs[ e[0] ]
		site_edge = ( e[1], e[2] )
		s0 = lneq[3]
		s1 = lneq[4]
		site_edges[ s0 ].append( site_edge )
		site_edges[ s1 ].append( site_edge )

	#print [ len(x) for x in site_edges ]


s = 20.0
def output_edges_points( verts, edges, pnts ) :
	for e in edges :
		v0 = verts[ e[1] ]
		v1 = verts[ e[2] ]
		v0outside = v0[0] < xlo or v0[0] > xhi or v0[1] < ylo or v0[1] > yhi
		v1outside = v1[0] < xlo or v1[0] > xhi or v1[1] < ylo or v1[1] > yhi
		if not v0outside or not v1outside :
			print "  <path d=\"M %f %f L %f %f\" stroke=\"blue\" stroke-width=\"0.08\" />" % ( s*v0[0], s*v0[1], s*v1[0], s*v1[1] )

	for p in pnts:
		print "  <path d=\"M %f %f L %f %f M %f %f L %f %f\" stroke=\"red\" stroke-width=\"0.04\" />" % ( s*p[0]-0.2,s*p[1], s*p[0]+0.2, s*p[1], s*p[0],s*p[1]-0.2, s*p[0],s*p[1]+0.2 )


def output( verts, edges, lneqs, pnts ) :

	edges = clip_edges( verts, edges, lneqs, pnts )

	add_border_edges( verts, edges )

	assemble_polygons( verts, edges, lneqs, pnts )

	print\
	'<?xml version="1.0" standalone="no"?>\n' \
	'<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n' \
	'<svg width="40pt" height="40pt" viewBox="-20 -20 40 40" xmlns="http://www.w3.org/2000/svg" version="1.1">\n'

	output_edges_points( verts, edges, pnts )
	
	print "</svg>"


if __name__ == "__main__" :
	lines = sys.stdin.readlines()

	verts = [ x.strip().split(' ')[1:] for x in lines if "v " in x ]
	verts = [ ( float(x[0]), float(x[1]) ) for x in verts ]

	edges = [ x.strip().split(' ')[1:] for x in lines if "e " in x ]
	edges = [ ( int(x[0]), int(x[1]), int(x[2]) ) for x in edges ]

	lneqs = [ x.strip().split(' ')[1:] for x in lines if "l " in x ]
	lneqs = [ ( float(x[0]), float(x[1]), float(x[2]), int(x[3]), int(x[4] ) ) for x in lneqs ]

	pnts  = [ x.strip().split(' ')[1:] for x in lines if "s " in x ]
	pnts  = [ ( float(x[0]), float(x[1]) ) for x in pnts ]

	output( verts, edges, lneqs, pnts )

