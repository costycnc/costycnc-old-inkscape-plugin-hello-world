#!/usr/bin/env python 

import inkex, cubicsuperpath, simplepath, cspsubdiv, os.path, time,sys

import math
import simplestyle
from simpletransform import composeTransform, fuseTransform, parseTransform, applyTransformToPath, applyTransformToPoint, formatTransform


	
class MyEffect(inkex.Effect):



	def __init__(self):
		inkex.Effect.__init__(self)
	
	def effect(self): 


		for id, shape in self.selected.items():
			self.recursiveFuseTransform(shape, parseTransform(None))
			#inkex.debug("sunt in shape")
				
		to_mm = lambda value: self.uutounit(value, 'mm')	
		doc_heigh=to_mm(self.unittouu(self.document.getroot().get('height')))
		gcode = ""
		pathc=[[0,0]]
		path_all= []
		path_one= []
		

		i = 0
		for id, node in self.selected.iteritems():
			if node.tag == inkex.addNS('path','svg'):
				self.recursiveFuseTransform(shape, parseTransform(None))
				d = node.get('d')
				p = cubicsuperpath.parsePath(d)
				cspsubdiv.cspsubdiv(p, 0.1)

				for sp in p:
					for csp in sp:
						path_one.append([csp[0][0],doc_heigh-csp[0][1]])
					path_all.append(path_one)
					path_one=[]

				num0=0
				num1=0
				num2=0
				currDiff=0
				path_final=[[0,0]];
				
	
				while len(path_all):	
				
					minDiff = sys.maxint;
					for i in range(len(path_final)):
						for m in range(len(path_all)):
							for n in range(len(path_all[m])):
								x=path_final[i][0]
								y=path_final[i][1]
								x1=path_all[m][n][0]
								y1=path_all[m][n][1]						
								x2=x-x1
								y2=y-y1
								currDiff = x2*x2+y2*y2						
								if currDiff < minDiff :
									minDiff = currDiff
									pos0 = i
									pat1 = m
									pos1 = n
					p_tmp=path_all.pop(pat1)		#extract
					p_tmp=p_tmp[pos1:]+p_tmp[:pos1]
					p_tmp=p_tmp+p_tmp[:1]
					path_final=path_final[:pos0+1]+p_tmp+path_final[pos0:]
					#path_final[:pos0+1] because read until pos0 and need to read also pos0
		
				gcode = "M3 S255\n"
				gcode +="G01 X0 Y0\n"
				i=0
				for i in range(len(path_final)-1):
					gcode += "G01 X" +str(round(self.uutounit(path_final[i][0], "mm" ),2)) + " Y" + str(round(self.uutounit(path_final[i][1], "mm" ),2)) + "\n"


		
		gcode +="G01 X0 Y0\n"
		f = open("costycnc.nc", 'w')
		inkex.debug(gcode)
		f.write(str(gcode))
		f.close()
		

	@staticmethod
	def objectToPath(node):
		if node.tag == inkex.addNS('g', 'svg'):
			return node

		if node.tag == inkex.addNS('path', 'svg') or node.tag == 'path':
			for attName in node.attrib.keys():
				if ("sodipodi" in attName) or ("inkscape" in attName):
					del node.attrib[attName]
			return node

		return node

	def scaleStrokeWidth(self, node, transf):
		if 'style' in node.attrib:
			style = node.attrib.get('style')
			style = simplestyle.parseStyle(style)
			update = False

			if 'stroke-width' in style:
				try:
					stroke_width = self.unittouu(style.get('stroke-width').strip())
					# pixelsnap ext assumes scaling is similar in x and y
					# and uses the x scale...
					# let's try to be a bit smarter
					# the least terrible option is using the geometric mean
					stroke_width *= math.sqrt(abs(transf[0][0] * transf[1][1]))
					style['stroke-width'] = str(stroke_width)
					update = True
				except AttributeError:
					pass

			if update:
				style = simplestyle.formatStyle(style)
				node.attrib['style'] = style

	def recursiveFuseTransform(self, node, transf=[[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]):
		transf = composeTransform(transf, parseTransform(node.get("transform", None)))

		if 'transform' in node.attrib:
			del node.attrib['transform']

		node = self.objectToPath(node)

		if 'd' in node.attrib:
			d = node.get('d')
			p = cubicsuperpath.parsePath(d)
			applyTransformToPath(transf, p)
			node.set('d', cubicsuperpath.formatPath(p))

			self.scaleStrokeWidth(node, transf)

		elif node.tag in [inkex.addNS('polygon', 'svg'),
						  inkex.addNS('polyline', 'svg')]:
			points = node.get('points')
			points = points.strip().split(' ')
			for k,p in enumerate(points):
				if ',' in p:
					p = p.split(',')
					p = [float(p[0]),float(p[1])]
					applyTransformToPoint(transf, p)
					p = [str(p[0]),str(p[1])]
					p = ','.join(p)
					points[k] = p
			points = ' '.join(points)
			node.set('points', points)

			self.scaleStrokeWidth(node, transf)

		elif node.tag in [inkex.addNS('rect', 'svg'),
						  inkex.addNS('text', 'svg'),
						  inkex.addNS('image', 'svg'),
						  inkex.addNS('use', 'svg'),
						  inkex.addNS('circle', 'svg')]:
			node.set('transform', formatTransform(transf))

		else:
			# e.g. <g style="...">
			self.scaleStrokeWidth(node, transf)

		for child in node.getchildren():
			self.recursiveFuseTransform(child, transf)
	
		
if __name__ == '__main__':
	e = MyEffect()
	e.affect()


