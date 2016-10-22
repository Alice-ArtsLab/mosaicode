#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.javascript.webaudio.webaudioplugin import WebaudioPlugin


class Speaker(WebaudioPlugin):

    # --------------------------------------------------------------------------
    def __init__(self):
        WebaudioPlugin.__init__(self)

        # Appearance
        self.help = "Sound output"
        self.label = "Speaker"
        self.icon = "images/show.png"
        self.color = "150:150:250:150"
        self.in_types = ["HRP_WEBAUDIO_SOUND"]
        self.group = "Sound"

        self.vars = """
// block_$id$ = Speaker
var block_$id$_i = []
block_$id$_i[0] = context.destination;
"""
