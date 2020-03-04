#!/usr/bin/env python

import sys
sys.path.append('/usr/share/inkscape/extensions')

# We will use the inkex module with the predefined Effect base class.
import inkex
from simplestyle import *
from simplepath import *
from math import sqrt
import simpletransform
import cubicsuperpath


class costycnc(inkex.Effect):

	def __init__(self):

		inkex.Effect.__init__(self)
		  


	def effect(self):

		output_nodes = ""
		i=1
		for node in self.selected.items():
			for id, node in self.selected.items():
				if node.tag == inkex.addNS('path','svg'):
					output_nodes += ""
					simpletransform.fuseTransform(node)
					d = node.get('d')
					p = cubicsuperpath.parsePath(d)
					for subpath in p:
						for csp in subpath:
							output_nodes += "G01 X" +str(csp[1][0]) + " Y" + str(csp[1][1]) + "\n"
		inkex.debug(output_nodes)        
		f = open("costycnc-inkscape.nc", 'w')
		f.write(output_nodes)
		f.close()
			
			
	
# Create effect instance and apply it.
effect = costycnc()
effect.affect()
