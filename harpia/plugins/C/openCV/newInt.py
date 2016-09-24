#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin

class NewInt(OpenCVPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.intVal = 1

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Creates new literal value (Int)"

    # ----------------------------------------------------------------------
    def generate_vars(self):
        self.intVal = int(self.intVal)
        return 'int  block$id$_int_o0 = $intVal$; // New Int Out\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {'Label': _('New Int'),
            'Icon': 'images/newDouble.png',
            'Color': '50:50:200:150',
            'InTypes': "",
            'OutTypes': {0: 'HRP_INT'},
            'TreeGroup': _('Basic Data Type')
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
                            }
        }

# ------------------------------------------------------------------------------
