#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class NewInt(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        self.id = -1
        self.type = "702"
        self.intVal = 1

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Creates new literal value (Int)"

    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):

        blockTemplate.imagesIO = 'int  block$$_int_o1 = ' + str(int(float(self.intVal))) + '; // New Int Out\n'

        blockTemplate.functionCall = ''

        blockTemplate.dealloc = ''

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            'Label': _('New Int'),
            'Icon': 'images/newDouble.png',
            'Color': '50:50:200:150',
            'InTypes': "",
            'OutTypes': {0: 'HRP_INT'},
            'Description': _('Creates new literal value (int)'),
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
                            }
        }

# ------------------------------------------------------------------------------
