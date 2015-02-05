#!/usr/bin/python

# Generates an animation where a 2,3-Halton sequence is expanded point by point, showing the Voronoi regions.
# Requires: imagemagick

import sys
import os


for fr in range(32) :
	cmd = "tail -%d ../testdata/2,3-halton.points | ../testforvor | ./mksvg.py > fr%02d.svg" % ( 4+fr, fr )
	os.system( cmd )
	cmd = "convert -density 240 fr%02d.svg fr%02d.png" % ( fr, fr )
	os.system( cmd )

cmd = "convert -delay 40 -loop 0 fr??.png anim.gif"
os.system( cmd )


