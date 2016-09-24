#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin

class intValue(OpenCVPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.intVal = 1
        self.maxVal = 31
        self.label = "Value"
        self.window_name = "My Image"

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Creates Slider to int value"

    # ----------------------------------------------------------------------
    def generate_vars(self):
        self.intVal = int(self.intVal)
        return \
            'int  block$id$_int_o0 = $intVal$; // New Int Out\n'

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return \
            'cvNamedWindow("$window_name$",CV_WINDOW_AUTOSIZE );\n' + \
            'cvCreateTrackbar("$label$", "$window_name$", &block$id$_int_o0, $maxVal$, NULL);\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {'Label': _('Int Value'),
            'Icon': 'images/newDouble.png',
            'Color': '50:50:200:150',
            'InTypes': "",
            'OutTypes': {0: 'HRP_INT'},
            'TreeGroup': _('Basic Data Type'),
            "IsSource": True
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {
            "intVal":{"name": "Value",
                        "type": HARPIA_INT,
                        "value": self.intVal,
                        "lower":0,
                        "upper":65535,
                        "step":1
                            },
            "maxVal":{"name": "Max Value",
                        "type": HARPIA_INT,
                        "value": self.maxVal,
                        "lower":0,
                        "upper":65535,
                        "step":1
                            },
            "label":{"name": "Label",
                    "type": HARPIA_STRING,
                    "value": self.label
            },                            
            "window_name": {"name": "Window Title",
                        "type": HARPIA_STRING,
                        "value": self.window_name
            }
        }

# ------------------------------------------------------------------------------
