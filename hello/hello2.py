#!/usr/bin/env python

import inkex

from simplestyle import *

class hello2(inkex.Effect):


    def effect(self):
        
        svg = self.document.getroot()
       
        layer = inkex.etree.SubElement(svg, 'g')
        layer.set(inkex.addNS('label', 'inkscape'), 'hello test')
        layer.set(inkex.addNS('groupmode', 'inkscape'), 'layer')

        # Create text element
        text = inkex.etree.Element(inkex.addNS('text','svg'))
        text.text = 'Hello test1'


        # Connect elements together.
        layer.append(text)

# Create effect instance and apply it.
effect = hello2()
effect.affect()