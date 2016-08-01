#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.s2icommonproperties import APP, DIR
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class IsOnRect(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        self.id = -1
        self.type = "902"

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Checks Wheather the given point is inside the given rectangle"
    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):
        blockTemplate.imagesIO = 'CvRect block$$_rect_i2;\n' + \
                                 'CvPoint block$$_point_i1;\n' + \
                                 'double block$$_double_o1;\n'
        blockTemplate.functionCall = '\n block$$_double_o1 = 0.0;\n' + \
                            'if(block$$_point_i1.x >= block$$_rect_i2.x)\n' + \
                            '	if(block$$_point_i1.y >= block$$_rect_i2.y)\n' + \
                            '		if(block$$_point_i1.x < block$$_rect_i2.x + block$$_rect_i2.width)\n' + \
                            '			if(block$$_point_i1.y < block$$_rect_i2.y + block$$_rect_i2.height)\n' + \
                            '				block$$_double_o1 = 1.0;\n'
        blockTemplate.dealloc = ''

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            'Label': _('Check Point'),
            'Icon': 'images/isOnRect.png',
            'Color': '50:50:200:150',
            'InTypes': {0: 'HRP_POINT', 1: 'HRP_RECT'},
            'OutTypes': {0: 'HRP_DOUBLE'},
            'Description': _('Checks Wheather the given point is inside the given rectangle'),
            'TreeGroup': _('Experimental')
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {}

# ------------------------------------------------------------------------------
