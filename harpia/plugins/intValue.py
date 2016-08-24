#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class intValue(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)
        self.id = -1
        self.type = "1702"
        self.intVal = 1
        self.maxVal = 65535
        self.label = "Value"
        self.window_name = "My Image"

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Creates Slider to int value"

    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):

        blockTemplate.imagesIO = 'int  block$$_int_o1 = ' + str(int(float(self.intVal))) + '; // New Int Out\n'

        blockTemplate.functionCall = 'cvNamedWindow("' + self.window_name + '",CV_WINDOW_AUTOSIZE );\n' + \
            'cvCreateTrackbar("' + self.label + '", "' + self.window_name + '", &block$$_int_o1, ' + str(int(float(self.maxVal))) + ', NULL);\n'

        blockTemplate.dealloc = ''

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            'Label': _('Int Value'),
            'Icon': 'images/newDouble.png',
            'Color': '50:50:200:150',
            'InTypes': "",
            'OutTypes': {0: 'HRP_INT'},
            'Description': _('Creates slider to Int Value'),
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
            "maxVal":{"name": "Value",
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
