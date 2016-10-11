#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.javascript.webaudio.webaudioplugin import WebaudioPlugin

class Speaker(WebaudioPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        WebaudioPlugin.__init__(self)
        self.help = "Sound output"
        self.vars = """
// block_$id$ = Speaker
var block_$id$_i = []
block_$id$_i[0] = context.destination;
"""
        self.description = {"Label": "Speaker",
            "Icon": "images/show.png",
            "Color": "150:150:250:150",
            "InTypes": {0: "HRP_WEBAUDIO_SOUND"},
            "OutTypes": {},
            "TreeGroup": "Sound"
            }
