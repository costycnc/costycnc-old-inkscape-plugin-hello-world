#!/usr/bin/env python

import inkex

from simplestyle import *

class HelloWorldEffect(inkex.Effect):
	def effect(self):
		inkex.debug("hello")
	

# Create effect instance and apply it.
effect = HelloWorldEffect()
effect.affect()
