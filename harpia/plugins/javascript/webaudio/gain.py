#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Gain class.
"""
from harpia.GUI.fieldtypes import *
from harpia.plugins.javascript.webaudio.webaudioplugin import WebaudioPlugin


class Gain(WebaudioPlugin):

    # --------------------------------------------------------------------------
    def __init__(self):
        WebaudioPlugin.__init__(self)

        # Appearance
        self.help = "Sound output"
        self.label = "Gain"
        self.color = "50:150:250:150"
        self.in_ports = [{"type":"HRP_WEBAUDIO_SOUND",
                           "label":"Sound Input",
                           "name":"sound_input"},
                        {"type":"HRP_WEBAUDIO_SOUND",
                           "label":"Gain Input",
                           "name":"gain_input"},
                        {"type":"HRP_WEBAUDIO_FLOAT",
                         "label":"Gain Value",
                         "name":"gain_value"}]
        self.out_ports = [{"type":"HRP_WEBAUDIO_SOUND",
                         "name":"sound_output",
                         "label":"Sound Output"}]
        self.group = "Sound"

        self.vars = """
// block_$id$ = Gain
var block_$id$ = context.createGain();
var block_$id$_o0 = null;
var block_$id$_i0 = block_$id$;
var block_$id$_i1 = block_$id$.gain;
var block_$id$_i2 = function(value){
    block_$id$.gain.value = value;
    };
"""

        self.function_call = "block_$id$_o0 = block_$id$;\n" + \
            "block_$id$.gain.value = $prop[gain]$;\n"

        self.properties = [{"name": "gain",
                            "label": "Gain",
                            "type": HARPIA_FLOAT,
                            "lower": 0,
                            "upper": 32000,
                            "value": 1
                            }
                           ]
