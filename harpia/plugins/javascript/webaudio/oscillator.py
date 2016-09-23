#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class Oscillator(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)
        self.id = -1
        self.freq = 440
        self.type = self.__class__.__module__
        self.oscillator_type = 'sine'

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Sound output"

    # ----------------------------------------------------------------------
    def generate_header(self):
        return ""

    # ----------------------------------------------------------------------
    def generate_vars(self):
        return """
var block_$id$ =  context.createOscillator();
var block_$id$_i = [];
block_$id$_i[1] = block_$id$.frequency;
block_$id$_i[2] = function(value){
    block_$id$.frequency.value = value;
};
block_$id$_i[3] = function(value){
    oscillator = ''
    if (value < 1) oscillator = 'square';
    if (value == 1) oscillator = 'sine';
    if (value == 2) oscillator = 'sawtooth';
    if (value > 2) oscillator = 'triangle';
    block_$id$.type = oscillator;
};
"""

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return """
block_$id$.type = '$oscillator_type$';
block_$id$.frequency.value = $freq$; // value in hertz
block_$id$.detune.value = 100; // value in cents
block_$id$.start(0);
"""

    # ----------------------------------------------------------------------
    def generate_dealloc(self):
        return "Oi, eu sou o oscilador."

    # ----------------------------------------------------------------------
    def generate_out_dealloc(self):
        return ""

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            "Label": _("Oscillator"),
            "Icon": "images/show.png",
            "Color": "50:150:250:150",
            "InTypes": {0: "HRP_WEBAUDIO_SOUND", 1: "HRP_WEBAUDIO_FLOAT", 2: "HRP_WEBAUDIO_FLOAT"},
            "OutTypes": {0: "HRP_WEBAUDIO_SOUND"},
            "Description": _("Sound Oscillator"),
            "TreeGroup": _("Sound"),
            "IsSource": True
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {"freq":{"name": "Frequency",
                    "type": HARPIA_FLOAT,
                    "value": self.freq,
                    "lower":20,
                    "upper":20000,
                    "step":1
                    },
                "oscillator_type":{"name": "Type",
                    "type": HARPIA_COMBO,
                    "value": self.oscillator_type,
                    "values": ["square", "sine", "sawtooth", "triangle"]
                    }
            }

# ------------------------------------------------------------------------------
