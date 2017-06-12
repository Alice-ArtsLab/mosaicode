#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the FloatValue class.
"""
from mosaicode.GUI.fieldtypes import *
from mosaicode.model.plugin import Plugin

class FloatValue(Plugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)

        self.language = "javascript"
        self.framework = "webaudio"
        self.help = "Double value"
        self.label = "FloatValue"
        self.color = "50:150:250:150"
        self.out_ports = [{"type":"mosaicode.extensions.javascript.ports.float",
                "label":"Float",
                "name":"float"}
            ]
        self.group = "Interface"

        self.properties = [{"name": "value",
                            "label": "Value",
                            "type": MOSAICODE_FLOAT,
                            "lower": 0,
                            "upper": 20000,
                            "step": 1,
                            "value": 1
                            },
                           {"name": "min",
                            "label": "Min",
                            "type": MOSAICODE_FLOAT,
                            "lower": 0,
                            "upper": 20000,
                            "step": 1,
                            "value": 1
                            },
                           {"name": "max",
                            "label": "Max",
                            "type": MOSAICODE_FLOAT,
                            "lower": 00,
                            "upper": 20000,
                            "step": 1,
                            "value": 10
                            },
                           {"name": "label",
                            "label": "Label",
                            "type": MOSAICODE_STRING,
                            "value": "Label"
                            }
                           ]

        self.codes[1] = """
// block_$id$ = Float Value
var block_$id$_value = $prop[value]$;
var $out_ports[float]$ = [];
"""
        self.codes[2] = """
function change_$id$_value(){
    value = document.getElementById("block_$id$").value;
    for (var i = 0; i < $out_ports[float]$.length ; i++){
        $out_ports[float]$[i](value);
    }
};
"""
        self.codes[3] = """
$prop[label]$ <input type="number" id="block_$id$" value="$prop[value]$" min="$prop[min]$"
        max="$prop[max]$" onChange="change_$id$_value();"><br>
"""

