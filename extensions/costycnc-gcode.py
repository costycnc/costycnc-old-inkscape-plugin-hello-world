#!/usr/bin/env python 

import inkex, cubicsuperpath, simplepath, cspsubdiv

def rotate(input,d): 
   # Slice string in two parts for left and right
	inkex.debug("rotate")
	inkex.debug(d)
	inkex.debug("finish rotate")
	Lfirst = input[0 : d] 
	Lsecond = input[d :] 
	Rfirst = input[0 : len(input)-d] 
	Rsecond = input[len(input)-d : ] 
	total = Lsecond + Lfirst  
	#total = input
	return total



class MyEffect(inkex.Effect):
	def __init__(self):
		inkex.Effect.__init__(self)
		self.OptionParser.add_option("-t", "--setup", action="store", type="string",
									 dest="setup", default="new", help=("Settings"))
		self.OptionParser.add_option("-f", "--flatness",
						action="store", type="int", 
						dest="flat", default=1,
						help="Minimum flatness of the subdivided curves")									
			
	def effect(self):
		setup = self.options.setup
		#inkex.debug(setup)
		pathNodes = self.document.xpath('//svg:line',namespaces=inkex.NSS)
		for cPathNode in pathNodes:
			cPathNode.getparent().remove(cPathNode)
	
		for id, node in self.selected.iteritems():
			#inkex.debug(node.get('id'))
			
			if node.tag == inkex.addNS('path','svg'):
				first = True
				gcode = ("M3 S255\nG90\n")#+"G01 F500.000\n"
				d = node.get('d')
				p = cubicsuperpath.parsePath(d)
				#subdivide dots points in .1 parts
				cspsubdiv.cspsubdiv(p, .1)   
				#find low y value
				
				cp = []                				
				g=0
				h=0
				if setup=='left':
					c=p[0][0][0][0]               
					for csp in p[0]:                   
						b = csp[0][0]
						e = csp[0][1]
						if (b < c):
							c = b
							f = e 
							h = g
						cp.append([[csp[0][0],csp[0][1]]])
						g += 1  
				if setup=='up':
					f=p[0][0][0][1]               
					for csp in p[0]:                   
						b = csp[0][0]
						e = csp[0][1]
						if (e < f):
							c = b
							f = e 
							h = g
						cp.append([[csp[0][0],csp[0][1]]])
						g += 1 
				if setup=='down':
					f=0 
					e=0
					for csp in p[0]: 
						cp.append([[csp[0][0],csp[0][1]]])                    
						if (e > f):
							c = b
							f = e 
							h = g
						b = csp[0][0]
						e = csp[0][1] 
						g += 1 
				if setup=='right':
					c=0 
					b=0
					for csp in p[0]: 
						cp.append([[csp[0][0],csp[0][1]]])                    
						if (b > c):
							c = b
							f = e 
							h = g
						b = csp[0][0]
						e = csp[0][1] 
						g += 1 
				if setup=='manual':
					h=int(self.options.flat)
					for csp in p[0]: 
						cp.append([[csp[0][0],csp[0][1]]]) 
				'''
				b=0
				e=0
				g=0
				c=p[0][0][0][0]
				f=0
				h=0
				cp = []               
				for csp in p[0]:                   
					b = csp[0][0]
					e = csp[0][1]
					if (b < c):
						c = b
						f = e 
						h = g
					cp.append([[csp[0][0],csp[0][1]]])
					g += 1  
				'''    
				np1 = []
				Lfirst = cp[0 : h] 
				Lsecond = cp[h :]
				np1 = Lsecond + Lfirst
				for csp in np1:
					cmd = 'L'                
					if first:
						x=str(round(self.uutounit(csp[0][0],"mm" ),2))
						y=str(round(self.uutounit(csp[0][1],"mm" ),2))
						line1 = inkex.etree.SubElement(self.current_layer, inkex.addNS('line','svg'), {'id': 'costy', 'x1': '0', 'y1': '0', 'style': 'stroke-width:1;stroke:red', 'x2': x, 'y2': y} ) 	
						gcode1 = "G01 X" + x + " Y" + y + "\n"
						gcode += gcode1						#line1 = inkex.etree.SubElement(self.current_layer, inkex.addNS('line','svg'), {'id': 'costy1','x1': '0', 'y0': '0', 'style': 'stroke-width:1;stroke:red', 'x2': x, 'y2': y} ) 	
					first = False	
					gcode += "G01 X" +str(round(self.uutounit(csp[0][0],"mm" ),2)) + " Y" + str(round(self.uutounit(csp[0][1],"mm" ),2)) + "\n"
				gcode += "G01 X" + x + " Y" + y + "\n"
				gcode += "G01 X0 Y0\n"
				f = open("costycnc.nc", 'w')
				f.write(str(gcode))
				f.close()	
				#if (node.attrib['id']=='costy'):
					#cPathNode.getparent().remove(cPathNode)
if __name__ == '__main__':
	e = MyEffect()
	e.affect()


# vim: expandtab shiftwidth=4 tabstop=8 softtabstop=4 fileencoding=utf-8 textwidth=99
