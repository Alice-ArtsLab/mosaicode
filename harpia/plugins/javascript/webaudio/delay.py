#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class Delay(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)
        self.time = 0
    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Sound output"

    # ----------------------------------------------------------------------
    def generate_header(self):
        return ""

    # ----------------------------------------------------------------------
    def generate_vars(self):
        return """
// block_$id$ = Delay
var block_$id$ = context.createDelay();
var block_$id$_i = []
block_$id$_i[0] = block_$id$
block_$id$_i[0].delayTime.value = $time$;
"""

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return """
"""

    # ----------------------------------------------------------------------
    def generate_dealloc(self):
        return ""

    # ----------------------------------------------------------------------
    def generate_out_dealloc(self):
        return ""

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Label": "Delay",
            "Icon": "images/show.png",
            "Color": "150:150:250:150",
            "InTypes": {0: "HRP_WEBAUDIO_SOUND"},
            "OutTypes": {0: "HRP_WEBAUDIO_SOUND"},
            "TreeGroup": "Sound"
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {"time":{"name": "Time",
                    "type": HARPIA_FLOAT,
                    "lower":0,
                    "upper":10000,
                    "step":1
                    }
            }

# ------------------------------------------------------------------------------
