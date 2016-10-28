#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.javascript.webaudio.webaudioplugin import WebaudioPlugin


class FloatValue(WebaudioPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        WebaudioPlugin.__init__(self)
        self.value = 1
        self.label = "Label"
        self.min = 0
        self.max = 10

        # Appearance
        self.help = "Double value"
        self.label = "FloatValue"
        self.icon = "images/show.png"
        self.color = "50:150:250:150"
        self.out_types = ["HRP_WEBAUDIO_FLOAT"]
        self.group = "Interface"

        self.vars = """
// block_$id$ = Float Value
var block_$id$_value = $value$;
var block_$id$_o0 = [];
"""
        self.function_call = """
function change_$id$_value(){
    value = document.getElementById("block_$id$").value;
    for (var i = 0; i < block_$id$_o0.length ; i++){
        block_$id$_o0[i](value);
    }
};
"""
        self.dealloc = """
$label$ <input type="number" id="block_$id$" value="$value$" min="$min$"
        max="$max$" onChange="change_$id$_value();"><br>
"""

        self.properties = {"value": {"name": "Value",
                                     "type": HARPIA_FLOAT,
                                     "lower": 0,
                                     "upper": 20000,
                                     "step": 1
                                     },
                           "min": {"name": "Min",
                                   "type": HARPIA_FLOAT,
                                   "lower": 0,
                                   "upper": 20000,
                                   "step": 1
                                   },
                           "max": {"name": "Max",
                                   "type": HARPIA_FLOAT,
                                   "lower": 00,
                                   "upper": 20000,
                                   "step": 1
                                   },
                           "label": {"name": "Label",
                                     "type": HARPIA_STRING
                                     }
                           }
