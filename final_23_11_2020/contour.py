#!/usr/bin/env python 

import inkex, cubicsuperpath, simplepath, cspsubdiv, os.path, time,sys,re
from applytransform import ApplyTransform 


	
class MyEffect(inkex.Effect):



	def __init__(self):
		inkex.Effect.__init__(self)
	
	def effect(self): 
	

		

		for id, node in self.selected.iteritems():
			if node.tag == inkex.addNS('path','svg'):
				d = node.get('d')
				x=[]
				x=re.split('[Mm]', d)
				#x = d.split("M")
				#inkex.debug(x[1])
				x="M"+x[1]

		

				node.set('d',x)


if __name__ == '__main__':
	e = MyEffect()
	e.affect()


# vim: expandtab shiftwidth=4 tabstop=8 softtabstop=4 fileencoding=utf-8 textwidth=99
