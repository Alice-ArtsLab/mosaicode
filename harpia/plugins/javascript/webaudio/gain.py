#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class Gain(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)
        self.id = -1
        self.type = self.__class__.__module__
        self.gain = 1

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Sound output"

    # ----------------------------------------------------------------------
    def generate_header(self):
        return ""

    # ----------------------------------------------------------------------
    def generate_vars(self):
        return """
var block_$id$ = context.createGain();
var block_$id$_i = [];
block_$id$_i[1] = block_$id$;
block_$id$_i[2] = block_$id$.gain;
block_$id$_i[3] = function(value){
    block_$id$.gain.value = value;
    };
"""

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return "block_$id$.gain.value = $gain$;\n"

    # ----------------------------------------------------------------------
    def generate_dealloc(self):
        return ""

    # ----------------------------------------------------------------------
    def generate_out_dealloc(self):
        return ""

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            "Label": _("Gain"),
            "Icon": "images/show.png",
            "Color": "50:150:250:150",
            "InTypes": {0: "HRP_WEBAUDIO_SOUND", 1: "HRP_WEBAUDIO_SOUND", 2: "HRP_WEBAUDIO_FLOAT"},
            "OutTypes": {0: "HRP_WEBAUDIO_SOUND"},
            "Description": _("Sound Gain"),
            "TreeGroup": _("Sound")
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {"gain":{"name": "Gain",
                    "type": HARPIA_FLOAT,
                    "value": self.gain,
                    "lower":0,
                    "upper":32000
                    }
                }

# ------------------------------------------------------------------------------
