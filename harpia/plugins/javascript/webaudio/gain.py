#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.javascript.webaudio.webaudioplugin import WebaudioPlugin


class Gain(WebaudioPlugin):

    # --------------------------------------------------------------------------
    def __init__(self):
        WebaudioPlugin.__init__(self)

        # Appearance
        self.help = "Sound output"
        self.label = "Gain"
        self.icon = "images/show.png"
        self.color = "50:150:250:150"
        self.out_types = ["HRP_WEBAUDIO_SOUND",
                          "HRP_WEBAUDIO_SOUND",
                          "HRP_WEBAUDIO_FLOAT"]
        self.group = "Sound"

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

        self.properties = [{"name": "gain",
                            "label": "Gain",
                            "type": HARPIA_FLOAT,
                            "lower": 0,
                            "upper": 32000,
                            "value":1
                                    }
                           ]
