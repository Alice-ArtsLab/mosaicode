#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class Gain(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)
        self.gain = 1

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Sound output"

    # ----------------------------------------------------------------------
    def generate_header(self):
        return ""

    # ----------------------------------------------------------------------
    def generate_vars(self):
        return """
// block_$id$ = Gain
var block_$id$ = context.createGain();
var block_$id$_i = [];
block_$id$_i[0] = block_$id$;
block_$id$_i[1] = block_$id$.gain;
block_$id$_i[2] = function(value){
    block_$id$.gain.value = value;
    };
"""

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return "block_$id$.gain.value = $gain$;\n"

    # ----------------------------------------------------------------------
    def generate_dealloc(self):
        return ""

    # ----------------------------------------------------------------------
    def generate_out_dealloc(self):
        return ""

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Label": "Gain",
            "Icon": "images/show.png",
            "Color": "50:150:250:150",
            "InTypes": {0: "HRP_WEBAUDIO_SOUND", 1: "HRP_WEBAUDIO_SOUND", 2: "HRP_WEBAUDIO_FLOAT"},
            "OutTypes": {0: "HRP_WEBAUDIO_SOUND"},
            "TreeGroup": "Sound"
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {"gain":{"name": "Gain",
                    "type": HARPIA_FLOAT,
                    "value": self.gain,
                    "lower":0,
                    "upper":32000
                    }
                }

# ------------------------------------------------------------------------------
