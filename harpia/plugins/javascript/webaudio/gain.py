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
                           "label":"Sound",
                           "name":"sound"},
                        {"type":"HRP_WEBAUDIO_SOUND",
                           "label":"Gain",
                           "name":"gain"},
                        {"type":"HRP_WEBAUDIO_FLOAT",
                         "label":"Gain Value",
                         "name":"gain_value"}]
        self.out_ports = [{"type":"HRP_WEBAUDIO_SOUND",
                         "name":"sound",
                         "label":"Sound"}]
        self.properties = [{"name": "gain",
                            "label": "Gain",
                            "type": HARPIA_FLOAT,
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
