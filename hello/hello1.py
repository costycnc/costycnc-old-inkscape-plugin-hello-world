#!/usr/bin/env python

import inkex
import simplepath
from lxml import etree

from simplestyle import *

class hello1(inkex.Effect):
	def __init__(self):
		inkex.Effect.__init__(self)
	def effect(self):
		
		for id, node in self.selected.iteritems():
			if node.tag == inkex.addNS('path','svg'):
				d = node.get('d')
				inkex.debug(d)
	

# Create effect instance and apply it.
effect = hello1()
effect.affect()
