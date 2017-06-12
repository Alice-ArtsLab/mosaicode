#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Gain class.
"""
from mosaicode.GUI.fieldtypes import *
from mosaicode.model.plugin import Plugin

class Gain(Plugin):

    # --------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)

        self.language = "javascript"
        self.framework = "webaudio"
        self.help = "Sound output"
        self.label = "Gain"
        self.color = "50:150:250:150"
        self.in_ports = [{"type":"mosaicode.extensions.javascript.ports.sound",
                           "label":"Sound",
                           "name":"sound"},
                        {"type":"mosaicode.extensions.javascript.ports.sound",
                           "label":"Gain",
                           "name":"gain"},
                        {"type":"mosaicode.extensions.javascript.ports.float",
                         "label":"Gain Value",
                         "name":"gain_value"}]
        self.out_ports = [{"type":"mosaicode.extensions.javascript.ports.sound",
                         "name":"sound",
                         "label":"Sound"}]
        self.properties = [{"name": "gain",
                            "label": "Gain",
                            "type": MOSAICODE_FLOAT,
                            "lower": 0,
                            "upper": 32000,
                            "value": 1
                            }
                           ]

        self.group = "Sound"

        self.codes[1] = """
// block_$id$ = $label$
var block_$id$ = context.createGain();
var $out_ports[sound]$ = null;
var $in_ports[sound]$ = block_$id$;
var $in_ports[gain]$ = block_$id$.gain;
var $in_ports[gain_value]$ = function(value){
    block_$id$.gain.value = value;
    };
"""

        self.codes[2] = "$out_ports[sound]$ = block_$id$;\n" + \
            "block_$id$.gain.value = $prop[gain]$;\n"
