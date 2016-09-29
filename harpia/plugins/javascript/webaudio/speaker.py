#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class Speaker(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Sound output"

    # ----------------------------------------------------------------------
    def generate_header(self):
        return ""

    # ----------------------------------------------------------------------
    def generate_vars(self):
        return """
// block_$id$ = Speaker
var block_$id$_i = []
block_$id$_i[0] = context.destination;
"""

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return """
"""

    # ----------------------------------------------------------------------
    def generate_dealloc(self):
        return ""

    # ----------------------------------------------------------------------
    def generate_out_dealloc(self):
        return ""

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Label": "Speaker",
            "Icon": "images/show.png",
            "Color": "150:150:250:150",
            "InTypes": {0: "HRP_WEBAUDIO_SOUND"},
            "OutTypes": {},
            "TreeGroup": "Sound"
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {}

# ------------------------------------------------------------------------------
