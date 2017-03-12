#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the FloatValue class.
"""
from harpia.GUI.fieldtypes import *
from harpia.plugins.javascript.webaudio.webaudioplugin import WebaudioPlugin


class FloatValue(WebaudioPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        WebaudioPlugin.__init__(self)

        self.help = "Double value"
        self.label = "FloatValue"
        self.color = "50:150:250:150"
        self.out_ports = [{"type":"HRP_WEBAUDIO_FLOAT",
                "label":"Float Value",
                "name":"float_value"}
            ]
        self.group = "Interface"

        self.properties = [{"name": "value",
                            "label": "Value",
                            "type": HARPIA_FLOAT,
                            "lower": 0,
                            "upper": 20000,
                            "step": 1,
                            "value": 1
                            },
                           {"name": "min",
                            "label": "Min",
                            "type": HARPIA_FLOAT,
                            "lower": 0,
                            "upper": 20000,
                            "step": 1,
                            "value": 1
                            },
                           {"name": "max",
                            "label": "Max",
                            "type": HARPIA_FLOAT,
                            "lower": 00,
                            "upper": 20000,
                            "step": 1,
                            "value": 10
                            },
                           {"name": "label",
                            "label": "Label",
                            "type": HARPIA_STRING,
                            "value": "Label"
                            }
                           ]

        self.vars = """
// block_$id$ = Float Value
var block_$id$_value = $prop[value]$;
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
$prop[label]$ <input type="number" id="block_$id$" value="$prop[value]$" min="$prop[min]$"
        max="$prop[max]$" onChange="change_$id$_value();"><br>
"""

