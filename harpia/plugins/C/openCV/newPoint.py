#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin

class NewPoint(OpenCVPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.x0 = 0
        self.y0 = 0

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Creates a new Point"

    # ----------------------------------------------------------------------
    def generate_vars(self):
        return 'CvPoint block$id$_point_o0 = cvPoint($x0$,$y0$);\n'

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return \
            'block$id$_point_o0 = cvPoint($x0$,$y0$);\n'

    # ----------------------------------------------------------------------
    def get_description(self):
        return {'Label': 'New Point',
            'Icon': 'images/newPoint.png',
            'Color': '50:50:200:150',
            'InTypes': "",
            'OutTypes': {0: 'HRP_POINT'},
            'TreeGroup': 'Basic Data Type'
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {
            "x0":{"name": "X",
                        "type": HARPIA_INT,
                        "value": self.x0,
                        "lower":0,
                        "upper":65535,
                        "step":1
                            },
            "y0":{"name": "Y",
                        "type": HARPIA_INT,
                        "value": self.y0,
                        "lower":0,
                        "upper":65535,
                        "step":1
                            }
            }

# ------------------------------------------------------------------------------
