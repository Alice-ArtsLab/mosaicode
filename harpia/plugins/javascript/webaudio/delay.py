#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.javascript.webaudio.webaudioplugin import WebaudioPlugin


class Delay(WebaudioPlugin):

    # --------------------------------------------------------------------------
    def __init__(self):
        WebaudioPlugin.__init__(self)
        self.time = 0

        # Appearance
        self.help = "Delay"
        self.label = "Delay"
        self.icon = "images/show.png"
        self.color = "150:150:250:150"
        self.in_types = ["HRP_WEBAUDIO_SOUND"]
        self.out_types = ["HRP_WEBAUDIO_SOUND"]
        self.group = "Sound"

        self.vars = """
// block_$id$ = Delay
var block_$id$ = context.createDelay();
var block_$id$_i = []
block_$id$_i[0] = block_$id$
block_$id$_i[0].delayTime.value = $time$;
"""

        self.properties = {"time": {"name": "Time",
                                    "type": HARPIA_FLOAT,
                                    "lower": 0,
                                    "upper": 10000,
                                    "step": 1
                                    }
                           }
