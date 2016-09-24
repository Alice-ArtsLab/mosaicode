#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin

class MoveRct(OpenCVPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.offset_x = 0
        self.offset_y = 0

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Move Rectangle`s (0,0) point to input point"

    # ----------------------------------------------------------------------
    def generate_vars(self):
        return \
            'CvRect block$id$_rect_i0;\n' + \
            'CvPoint block$id$_point_i1;\n' + \
            'CvRect block$id$_rect_o0;\n'

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return \
                'block$id$_rect_o0 = block$id$_rect_i0;\n' + \
                'block$id$_rect_o0.x = block$id$_point_i1.x + $offset_x$;\n' + \
                'block$id$_rect_o0.y = block$id$_point_i1.y + $offset_y$;\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {'Label': _('Move Rectangle'),
            'Icon': 'images/moveRct.png',
            'Color': '50:50:200:150',
            'InTypes': {0: 'HRP_RECT', 1: 'HRP_POINT'},
            'OutTypes': {0: 'HRP_RECT'},
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
