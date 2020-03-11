#!/usr/bin/env python 

import inkex, cubicsuperpath, simplepath, cspsubdiv, os.path, serial



class MyEffect(inkex.Effect):
	def __init__(self):
		inkex.Effect.__init__(self)
		self.OptionParser.add_option("-f", "--flatness",
						action="store", type="float", 
						dest="flat", default=0.1,
						help="Minimum flatness of the subdivided curves")
	def effect(self): 
		gcode = ""
		i = 0
		doc = self.document.getroot()
		factor = self.unittouu(doc.get('width'))        
		inkex.debug(factor) 
		
		for id, node in self.selected.iteritems():
			if node.tag == inkex.addNS('path','svg'):
				d = node.get('d')
				p = cubicsuperpath.parsePath(d)
				cspsubdiv.cspsubdiv(p, self.options.flat)
				np = []
				

				first = True
				gcode = "M3 S255(colona "+str(i)+") \n"#+"G01 F500.000\n"
					
				for csp in p[0]:
					cmd = 'L'
					if first:
						cmd = 'M'
					first = False
						
					np.append([cmd,[csp[1][0],csp[1][1]]])
					gcode += "G01 X" +str(csp[1][0]) + " Y" + str(csp[1][1]) + "\n"
					node.set('d',simplepath.formatPath(np))
				f = open("costycnc.nc", 'w')
				f.write(str(gcode))
				f.close()
if __name__ == '__main__':
	e = MyEffect()
	e.affect()


# vim: expandtab shiftwidth=4 tabstop=8 softtabstop=4 fileencoding=utf-8 textwidth=99
