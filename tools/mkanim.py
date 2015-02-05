#!/usr/bin/python

import sys
import os


for fr in range(128) :
	cmd = "tail -%d ../testdata/2,3-halton.points | ../testforvor | ./mksvg.py > fr%02d.svg" % ( 4+fr, fr )
	os.system( cmd )
	cmd = "convert -density 240 fr%02d.svg fr%02d.png" % ( fr, fr )
	os.system( cmd )

cmd = "convert -delay 20 -loop 0 fr??.png anim.gif"
os.system( cmd )


