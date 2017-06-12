#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Char2Float class.
"""
from mosaicode.GUI.fieldtypes import *
from mosaicode.model.plugin import Plugin

class Char2Float(Plugin):

    # --------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)

        self.language = "javascript"
        self.framework = "webaudio"
        self.help = "Char to Float"
        self.label = "Char 2 Float"
        self.color = "200:200:25:150"
        self.in_ports = [{"type":"mosaicode.extensions.javascript.ports.char",
                "label":"Char Input",
                "name":"char_input"}
                ]
        self.out_ports = [{"type":"mosaicode.extensions.javascript.ports.float",
                "label":"Float Output",
                "name":"float_output"}
            ]
        self.properties = [{"name": "float",
                            "label": "Output float",
                                     "type": MOSAICODE_FLOAT,
                                     "lower": 0,
                                     "upper": 20000,
                                     "step": 1,
                                     "value": 60
                            },
                           {"name": "char",
                            "label": "Input Char",
                            "type": MOSAICODE_STRING,
                            "value": "a"
                            }
                           ]
        self.group = "Conversion"

        self.codes[1] = """
// block_$id$ = Char 2 Float
var $out_ports[float_output]$ = [];
var $in_ports[char_input]$ = function(value){
    if (value != '$prop[char]$')
        return true;
    for (var i = 0; i < $out_ports[float_output]$.length ; i++){
        $out_ports[float_output]$[i]($prop[float]$);
    }
    return true;
    };
"""
