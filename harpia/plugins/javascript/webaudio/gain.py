#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.javascript.webaudio.webaudioplugin import WebaudioPlugin

class Gain(WebaudioPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        WebaudioPlugin.__init__(self)
        self.gain = 1
        self.help = "Sound output"
        self.vars = """
// block_$id$ = Gain
var block_$id$ = context.createGain();
var block_$id$_i = [];
block_$id$_i[0] = block_$id$;
block_$id$_i[1] = block_$id$.gain;
block_$id$_i[2] = function(value){
    block_$id$.gain.value = value;
    };
"""

        self.function_call = "block_$id$.gain.value = $gain$;\n"
        self.description = {"Label": "Gain",
            "Icon": "images/show.png",
            "Color": "50:150:250:150",
            "InTypes": {0: "HRP_WEBAUDIO_SOUND", 1: "HRP_WEBAUDIO_SOUND", 2: "HRP_WEBAUDIO_FLOAT"},
            "OutTypes": {0: "HRP_WEBAUDIO_SOUND"},
            "TreeGroup": "Sound"
            }

        self.properties = {"gain":{"name": "Gain",
                    "type": HARPIA_FLOAT,
                    "lower":0,
                    "upper":32000
                    }
                }
