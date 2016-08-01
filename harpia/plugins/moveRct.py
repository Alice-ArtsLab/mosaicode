#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.s2icommonproperties import APP, DIR
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class MoveRct(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        self.id = -1
        self.type = "803"
        self.offset_x = 0
        self.offset_y = 0

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Move Rectangle`s (0,0) point to input point"
    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):
        blockTemplate.imagesIO = 'CvRect block$$_rect_i1;\n' + \
                                 'CvPoint block$$_point_i2;\n' + \
                                 'CvRect block$$_rect_o1;\n'
        blockTemplate.functionCall = 'block$$_rect_o1 = block$$_rect_i1;\n' + \
                                     'block$$_rect_o1.x = block$$_point_i2.x + ' + self.offset_x + ';\n' + \
                                     'block$$_rect_o1.y = block$$_point_i2.y + ' + self.offset_y + ';\n'
        blockTemplate.dealloc = ''

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            'Label': _('Move Rectangle'),
            'Icon': 'images/moveRct.png',
            'Color': '50:50:200:150',
            'InTypes': {0: 'HRP_RECT', 1: 'HRP_POINT'},
            'OutTypes': {0: 'HRP_RECT'},
            'Description': _('Move Rectangle`s (0,0) point to input point'),
            'TreeGroup': _('Experimental')
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {
            "offset_x":{"name": "Offset x",
                        "type": HARPIA_INT,
                        "value": self.offset_x,
                        "lower":0,
                        "upper":65535,
                        "step":1
                            },

            "offset_y":{"name": "Offset Y",
                        "type": HARPIA_INT,
                        "value": self.offset_y,
                        "lower":0,
                        "upper":65535,
                        "step":1
                            }
        }

# ------------------------------------------------------------------------------
