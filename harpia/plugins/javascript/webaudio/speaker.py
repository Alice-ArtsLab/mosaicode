#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Speaker class.
"""
from harpia.GUI.fieldtypes import *
from harpia.plugins.javascript.webaudio.webaudioplugin import WebaudioPlugin


class Speaker(WebaudioPlugin):

    # --------------------------------------------------------------------------
    def __init__(self):
        WebaudioPlugin.__init__(self)

        # Appearance
        self.help = "Sound output"
        self.label = "Speaker"
        self.color = "150:150:250:150"
        self.in_ports = [{"type":"HRP_WEBAUDIO_SOUND",
                "label":"Sound Input",
                "name":"sound_input"}
            ]
        self.group = "Sound"

        self.vars = """
// block_$id$ = $label$
var block_$id$_i = []
block_$id$_i[0] = context.destination;
"""
