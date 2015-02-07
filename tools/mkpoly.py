#!/usr/bin/python

import sys
import os
import random

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
		# If edge goes to infinity, we should clip it, and introduce a new vertex.
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
				newe = ( e[0], e[1], newvertidx, e[3], e[4] ) if unkno == 2 else ( e[0], newvertidx, e[2], e[3], e[4] )
				newvertidx += 1
				accepted_edges.append( newe )

		# if both edge end points are in outside the rectangle, discard it.
		elif v0oob and v1oob :
			pass

		# if both edge end points are in inside the rectangle, pass through the edge as is.
		elif not v0oob and not v1oob :
			accepted_edges.append( e )

		# if start point is outside, clip the edge after introducing a new vertex.
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
			newe = ( e[0], newvertidx, e[2], e[3], e[4] )
			newvertidx += 1
			accepted_edges.append( newe )

		# if end point is outside, clip the edge after introducing a new vertex.
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
			newe = ( e[0], e[1], newvertidx, e[3], e[4] )
			newvertidx += 1
			accepted_edges.append( newe )

	return accepted_edges


"""
Determines which site is common for two edges.
Assumes that edges share a voronoi region.
"""
def common_site( ei0, ei1, edges ) :
	e0 = edges[ei0]
	e1 = edges[ei1]
	sites = ( e0[3], e0[4], e1[3], e1[4] )
	histo = [ ( sites.count( s ), s ) for s in sites ]
	site  = max( histo )[ 1 ]
	return site


"""
Take a sorted list of vertices that lie on a border, and create edges between them.
Note: skips first and last edge, as corner edges are special cases.
"""
def add_border( bl, edges, edgemap ) :
	for i in range( 1, len(bl) - 2 ) :
		vi0 = bl[i+0][2]
		vi1 = bl[i+1][2]
		el0 = edgemap[ vi0 ]
		el1 = edgemap[ vi1 ]
		assert len(el0) == 1
		assert len(el1) == 1
		site = common_site( el0[0], el1[0], edges )
		newe = ( -1, vi0, vi1, site, -1 )
		edges.append( newe )


"""
Add border edges between vertices that lie on le/ri/tp/bt border.
Also add border edges for the corner sites.
"""
def add_border_edges( verts, edges, edgemap ) :
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

	le = []	# all the vertices on the left border (x-)
	ri = []	# all the vertices on the right border (x+)
	bt = [] # all the vertices on the bottom border (y-)
	tp = [] # all the vertices on the top border (y+)

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


	# identify the corner sites.
	btle_site = btri_site = tple_site = tpri_site = -1

	if len(bt) > 2 and len(le) > 2 :
		vi0 = bt[  1 ][ 2 ]
		vi1 = le[  1 ][ 2 ]
		ei0 = edgemap[ vi0 ][ 0 ]
		ei1 = edgemap[ vi1 ][ 0 ]
		btle_site = common_site( ei0, ei1, edges )

	if len(bt) > 2 and len(ri) > 2 :
		vi0 = bt[ -2 ][ 2 ]
		vi1 = ri[  1 ][ 2 ]
		ei0 = edgemap[ vi0 ][ 0 ]
		ei1 = edgemap[ vi1 ][ 0 ]
		btri_site = common_site( ei0, ei1, edges )

	if len(tp) > 2 and len(le) > 2 :
		vi0 = tp[  1 ][ 2 ]
		vi1 = le[ -2 ][ 2 ]
		ei0 = edgemap[ vi0 ][ 0 ]
		ei1 = edgemap[ vi1 ][ 0 ]
		tple_site = common_site( ei0, ei1, edges )

	if len(tp) > 2 and len(ri) > 2 :
		vi0 = tp[ -2 ][ 2 ]
		vi1 = ri[ -2 ][ 2 ]
		ei0 = edgemap[ vi0 ][ 0 ]
		ei1 = edgemap[ vi1 ][ 0 ]
		tpri_site = common_site( ei0, ei1, edges )

	add_border( le, edges, edgemap )
	add_border( ri, edges, edgemap )
	add_border( bt, edges, edgemap )
	add_border( tp, edges, edgemap )

	if btle_site == -1 or btri_site == -1 or tple_site == -1 or tpri_site == -1 :
		sys.stderr.write( "Missing site identification for corner.\n" )

	# Now add the corner edges (8 in total)
	if btle_site > -1 :
		newe = ( -1, bt[  0 ][ 2 ], bt[  1 ][ 2 ], btle_site, -1 )
		edges.append( newe )
		newe = ( -1, le[  0 ][ 2 ], le[  1 ][ 2 ], btle_site, -1 )
		edges.append( newe )

	if btri_site > -1 :
		newe = ( -1, bt[ -1 ][ 2 ], bt[ -2 ][ 2 ], btri_site, -1 )
		edges.append( newe )
		newe = ( -1, ri[  0 ][ 2 ], ri[  1 ][ 2 ], btri_site, -1 )
		edges.append( newe )

	if tple_site > -1 :
		newe = ( -1, tp[  0 ][ 2 ], tp[  1 ][ 2 ], tple_site, -1 )
		edges.append( newe )
		newe = ( -1, le[ -1 ][ 2 ], le[ -2 ][ 2 ], tple_site, -1 )
		edges.append( newe )

	if tpri_site > -1 :
		newe = ( -1, tp[ -1 ][ 2 ], tp[ -2 ][ 2 ], tpri_site, -1 )
		edges.append( newe )
		newe = ( -1, ri[ -1 ][ 2 ], ri[ -2 ][ 2 ], tpri_site, -1 )
		edges.append( newe )


"""
Determine if these two edges share a common vertex.
"""
def common_vert( e0, e1 ) :
	return e0[0] == e1[0] or e0[0] == e1[1] or e0[1] == e1[0] or e0[1] == e1[1]


"""
Find an edge that shares a vertex with specified edge.
"""
def common_vert_from_list( e0, edgelist ) :
	for i in range( len(edgelist) ) :
		if common_vert( e0, edgelist[i] ) :
			e = edgelist[ i ]
			del edgelist[ i ]
			return e
	return None


"""
We have an unordered bag of edges.
Assign them to voronoi sites, and then order the edges in a loop around the voronoi site.
"""
def assemble_polygons( verts, edges, lneqs, pnts ) :

	numsites = len( pnts )
	site_edges = [ [] for x in range( numsites ) ]

	# Associate each site with bordering edges.
	for e in edges :
		site_edge = ( e[1], e[2] )
		s0 = e[3]
		s1 = e[4]
		if s0 > -1 :
			site_edges[ s0 ].append( site_edge )
		if s1 > -1 :
			site_edges[ s1 ].append( site_edge )

	# Chain edges together to form a polygon.
	polygons = []
	for sitenr, site in enumerate( site_edges ) :
		edgelist = site[1:]
		edgeseq  = site[:1]
		while edgelist :
			nxtedge = common_vert_from_list( edgeseq[-1], edgelist )
			if not nxtedge:
				edgelist=[]
			else:
				edgeseq.append( nxtedge )
		if len( edgeseq ) > 0 :
			v0 = edgeseq[0][0]
			v1 = edgeseq[0][1]
			poly = [ v0, v1 ] if v1 in edgeseq[1] else [ v1, v0 ]
			for e in edgeseq[1:] :
				poly.append( e[0] if poly[-1] != e[0] else e[1] )
			#sys.stderr.write( "edgeseq:" + str(edgeseq) + "\n" )
			#sys.stderr.write( "poly:" + str(poly) + "\n" )
			polygons.append( poly )
		else:
			sys.stderr.write( "edgeseq could not be determined for sitenr %d with %d edges.\n" % ( sitenr, len(site) ) )

	return polygons


def output_polygons( polygons ) :
	for p in polygons:
		print "p",
		for vi in p[:-1] :
			print vi,
		print ""

def output_verts( verts ) :
	for v in verts :
		print "v %f %f" % ( v[0], v[1] )

def output_points( pnts ) :
	for p in pnts:
		print "s %f %f" % ( p[0], p[1] )


def output( verts, edges, lneqs, pnts ) :
	# Clip edges and add a border.
	edges = clip_edges( verts, edges, lneqs, pnts )
	edgemap = create_edge_map( verts, edges )
	add_border_edges( verts, edges, edgemap )
	# Chain edges to create polygons.
	polygons = assemble_polygons( verts, edges, lneqs, pnts )
	# Write results to stdout
	output_points( pnts )
	output_verts( verts )
	output_polygons( polygons )


def create_edge_map( verts, edges ) :
	edgemap = [ [] for v in verts ]
	for edgenr, edge in enumerate(edges) :
		if edge[1] != -1 :
			edgemap[ edge[1] ].append( edgenr )
		if edge[2] != -1:
			edgemap[ edge[2] ].append( edgenr )
	return edgemap


if __name__ == "__main__" :
	argc = len( sys.argv )
	if argc != 1 and argc != 5 :
		sys.stderr.write( "usage: %s [minx miny maxx maxy] < diagraminput\n" % ( sys.argv[0] ) )
		sys.exit( 1 )
	if argc == 5 :
		xlo = float( sys.argv[ 1 ] )
		ylo = float( sys.argv[ 2 ] )
		xhi = float( sys.argv[ 3 ] )
		yhi = float( sys.argv[ 4 ] )

	lines = sys.stdin.readlines()

	verts = [ x.strip().split(' ')[1:] for x in lines if "v " in x ]
	verts = [ ( float(x[0]), float(x[1]) ) for x in verts ]

	lneqs = [ x.strip().split(' ')[1:] for x in lines if "l " in x ]
	lneqs = [ ( float(x[0]), float(x[1]), float(x[2]), int(x[3]), int(x[4] ) ) for x in lneqs ]

	edges = [ x.strip().split(' ')[1:] for x in lines if "e " in x ]
	edges = [ ( int(x[0]), int(x[1]), int(x[2]) ) for x in edges ]
	edges = [ ( e[0], e[1], e[2], lneqs[e[0]][ 3 ], lneqs[e[0]][ 4 ] ) for e in edges ]

	pnts  = [ x.strip().split(' ')[1:] for x in lines if "s " in x ]
	pnts  = [ ( float(x[0]), float(x[1]) ) for x in pnts ]

	output( verts, edges, lneqs, pnts )

