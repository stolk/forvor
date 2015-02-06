#!/usr/bin/python

import sys
import os
import random


def output_polygons( polygons, verts, s ) :
	for p in polygons:
		v0 = verts[ p[ 0 ] ]
		print '  <path d="M %f %f ' % ( s*v0[0], s*v0[1] ),
		for vi in p[1:] :
			v = verts[ vi ]
			print 'L %f %f ' % ( s*v[0], s*v[1] ),
		r = chr( int( random.uniform(65, 70) ) )
		g = chr( int( random.uniform(65, 70) ) )
		b = chr( int( random.uniform(65, 70) ) )
		rgb = r+g+b
		print 'z" stroke="black" fill="#%s" stroke-width="0.08" />' % ( rgb,  )


def output_points( pnts, s ) :
	for p in pnts:
		print '  <path d="M %f %f L %f %f M %f %f L %f %f" stroke="red" stroke-width="0.04" />' % ( s*p[0]-0.2,s*p[1], s*p[0]+0.2, s*p[1], s*p[0],s*p[1]-0.2, s*p[0],s*p[1]+0.2 )


if __name__ == "__main__" :
	lines = sys.stdin.readlines()

	verts = [ x.strip().split(' ')[1:] for x in lines if "v " in x ]
	verts = [ ( float(x[0]), float(x[1]) ) for x in verts ]

	pnts  = [ x.strip().split(' ')[1:] for x in lines if "s " in x ]
	pnts  = [ ( float(x[0]), float(x[1]) ) for x in pnts ]

	polys = [ x.strip().split(' ')[1:] for x in lines if "p " in x ]
	polys = [ map( lambda x: int(x), poly ) for poly in polys ]

	scl = 20.0

	print\
	'<?xml version="1.0" standalone="no"?>\n' \
	'<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n' \
	'<svg width="40pt" height="40pt" viewBox="-20 -20 40 40" xmlns="http://www.w3.org/2000/svg" version="1.1">\n'

	output_polygons( polys, verts, scl )
	output_points( pnts, scl )

	print "</svg>"

