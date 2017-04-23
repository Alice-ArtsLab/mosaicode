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
                "label":"Sound",
                "name":"sound"}
                ]
        self.out_ports = [{"type":"HRP_WEBAUDIO_SOUND",
                "label":"Sound",
                "name":"sound"}
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

        self.codes[1] = """
// block_$id$ = Delay
var block_$id$ = context.createDelay();
var $out_ports[sound]$ = null;
var $in_ports[sound]$ = null;
"""

        self.codes[2] = "$in_ports[sound]$ = block_$id$;\n" + \
            "var block_$id$.delayTime.value = $prop[time]$\n;" + \
            "$out_ports[sound]$ = block_$id$;\n"

