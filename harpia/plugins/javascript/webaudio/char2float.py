#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Char2Float class.
"""
from harpia.GUI.fieldtypes import *
from harpia.plugins.javascript.webaudio.webaudioplugin import WebaudioPlugin


class Char2Float(WebaudioPlugin):

    # --------------------------------------------------------------------------
    def __init__(self):
        WebaudioPlugin.__init__(self)

        # Appearance
        self.help = "Char to Float"
        self.label = "Char 2 Float"
        self.color = "200:200:25:150"
        self.in_ports = [{"type":"HRP_WEBAUDIO_CHAR",
                "label":"Char Input",
                "name":"char_input"}
                ]
        self.out_ports = [{"type":"HRP_WEBAUDIO_FLOAT",
                "label":"Float Output",
                "name":"float_output"}
            ]
        self.properties = [{"name": "float",
                            "label": "Output float",
                                     "type": HARPIA_FLOAT,
                                     "lower": 0,
                                     "upper": 20000,
                                     "step": 1,
                                     "value": 60
                            },
                           {"name": "char",
                            "label": "Input Char",
                            "type": HARPIA_STRING,
                            "value": "a"
                            }
                           ]
        self.group = "Conversion"

        self.vars = """
// block_$id$ = Char 2 Float
var block_$id$_o0 = [];
var block_$id$_i0 = function(value){
    if (value != '$prop[char]$')
        return true;
    for (var i = 0; i < block_$id$_o0.length ; i++){
        block_$id$_o0[i]($prop[float]$);
    }
    return true;
    };
"""
