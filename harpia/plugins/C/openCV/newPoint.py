#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class NewPoint(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)
        self.id = -1
        self.type = self.__class__.__module__
        self.x0 = 0
        self.y0 = 0

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Creates a new Point"
    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):
        blockTemplate.imagesIO = 'CvPoint block$id$_point_o1;\n'
        blockTemplate.functionCall = 'block$id$_point_o1 = cvPoint($x0$,$y0$);\n'
        blockTemplate.dealloc = ''

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            'Label': _('New Point'),
            'Icon': 'images/newPoint.png',
            'Color': '50:50:200:150',
            'InTypes': "",
            'OutTypes': {0: 'HRP_POINT'},
            'Description': _('Creates a new Point'),
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
                            }
            }

# ------------------------------------------------------------------------------
