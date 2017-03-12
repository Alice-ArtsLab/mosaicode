#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Delay class.
"""
from harpia.GUI.fieldtypes import *
from harpia.plugins.javascript.webaudio.webaudioplugin import WebaudioPlugin


class Delay(WebaudioPlugin):

    # --------------------------------------------------------------------------
    def __init__(self):
        WebaudioPlugin.__init__(self)

        # Appearance
        self.help = "Delay"
        self.label = "Delay"
        self.color = "150:150:250:150"
        self.in_ports = [{"type":"HRP_WEBAUDIO_SOUND",
                "label":"Sound Input",
                "name":"sound_input"}
                ]
        self.out_ports = [{"type":"HRP_WEBAUDIO_SOUND",
                "label":"Sound Output",
                "name":"sound_output"}
            ]

        self.group = "Sound"

        self.properties = [{"name": "time",
                            "label": "Time",
                            "type": HARPIA_FLOAT,
                            "lower": 0,
                            "upper": 10000,
                            "step": 1,
                            "value": 1
                            }
                           ]

        self.vars = """
// block_$id$ = Delay
var block_$id$ = context.createDelay();
var block_$id$_o0 = null;
var block_$id$_i0 = null;
"""

        self.function_call = "block_$id$_i0 = block_$id$;\n" + \
            "var block_$id$.delayTime.value = $prop[time]$\n;" + \
            "block_$id$_o0 = block_$id$;\n"

