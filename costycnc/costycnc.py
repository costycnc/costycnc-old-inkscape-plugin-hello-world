#!/usr/bin/env python

import inkex
import simplepath
from lxml import etree

from simplestyle import *
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
		inkex.debug("file 'costycnc.nc' is saved in Inkscape\Data\settings\extensions \n and contain:\n")  
		inkex.debug(output_nodes)         
		f = open("costycnc.nc", 'w')
		f.write(output_nodes)
		f.close()
			
	

# Create effect instance and apply it.
effect = costycnc()
effect.affect()
