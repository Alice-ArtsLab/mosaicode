#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Speaker class.
"""
from mosaicode.GUI.fieldtypes import *
from mosaicode.model.plugin import Plugin

class Speaker(Plugin):

    # --------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)

        self.language = "javascript"
        self.framework = "webaudio"
        self.help = "Sound output"
        self.label = "Speaker"
        self.color = "150:150:250:150"
        self.in_ports = [{"type":"mosaicode.extensions.javascript.ports.sound",
                "label":"Sound",
                "name":"sound"}
            ]
        self.group = "Sound"

        self.codes[1] = """
// block_$id$ = $label$
var $in_ports[sound]$ = context.destination;
"""
