#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class NewRect(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        self.id = -1
        self.type = "801"
        self.x0 = 0
        self.y0 = 0
        self.width = 640
        self.height = 480

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
       return "Creates new rectangle"

    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):
        blockTemplate.imagesIO = '\nCvRect block$$_rect_o1;\n'
        blockTemplate.functionCall = 'block$$_rect_o1 = cvRect(' + str(
            int(float(self.x0))) + ', ' + str(int(float(self.y0))) + ', ' + str(int(float(self.width))) + ', ' + str(int(float(self.height))) + ');'
        blockTemplate.dealloc = ''
    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            'Label': _('New Rectangle'),
            'Icon': 'images/newRect.png',
            'Color': '50:50:200:150',
            'InTypes': "",
            'OutTypes': {0: 'HRP_RECT'},
            'Description': _('Creates new rectangle'),
            'TreeGroup': _('Basic Data Type'),
            "IsSource": True
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
                            },
            "width":{"name": "Width",
                        "type": HARPIA_INT,
                        "value": self.width,
                        "lower":0,
                        "upper":65535,
                        "step":1
                            },
            "height":{"name": "Height",
                        "type": HARPIA_INT,
                        "value": self.height,
                        "lower":0,
                        "upper":65535,
                        "step":1
                            }
        }

# ------------------------------------------------------------------------------
