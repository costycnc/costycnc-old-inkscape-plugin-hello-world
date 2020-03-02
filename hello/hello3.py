#!/usr/bin/env python

import sys
sys.path.append('/usr/share/inkscape/extensions')

# We will use the inkex module with the predefined Effect base class.
import inkex
from simplestyle import *
from simplepath import *
from math import sqrt


class hello3(inkex.Effect):
    """
    Inkscape effect extension.
    Searches for paths that match and places them on the named layer.
    """
    def __init__(self):
        """
        Constructor.
        Defines the "--what" option of a script.
        """
        # Call the base class constructor.
        inkex.Effect.__init__(self)
          
        self.OptionParser.add_option('-f', '--textout', action = 'store',
          type = 'string', dest = 'textout', default = 'hello world!',
          help = 'Name of layer to put found objects on?') 


    def effect(self):
        """
        Effect behaviour.
        Search for all paths that match the selected path
        """
        textout = self.options.textout
                    
        f = open("costy.txt", 'w')
        f.write(textout)
        f.close()
            
            
        



# Create effect instance and apply it.
effect = hello3()
effect.affect()
