#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class Midi2Freq(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "midi to freq"

    # ----------------------------------------------------------------------
    def generate_header(self):
        return ""

    # ----------------------------------------------------------------------
    def generate_vars(self):
        return """
// block_$id$ = Midi 2 Freq
var block_$id$_o0 = [];
var block_$id$_i = [];

block_$id$_i[0] = function(value){
    value = (value < 0) ? 0 : value;
    value = (value >127) ? 127 : value;
    var arg = ((parseFloat(value) - 69.0) / 12.0);
    result =  Math.pow(2.0, arg) * 440.0;
    for (var i = 0; i < block_$id$_o0.length ; i++){
        block_$id$_o0[i](result);
    }
    return true;
    };
"""

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return """
"""

    # ----------------------------------------------------------------------
    def generate_dealloc(self):
        return """"""


    # ----------------------------------------------------------------------
    def generate_out_dealloc(self):
        return ""

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            "Label": _("Midi 2 Freq"),
            "Icon": "images/show.png",
            "Color": "200:200:25:150",
            "InTypes": {0: "HRP_WEBAUDIO_FLOAT"},
            "OutTypes": {0: "HRP_WEBAUDIO_FLOAT"},
            "Description": _("Midi 2 Freq"),
            "TreeGroup": _("Conversion")
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {}

# ------------------------------------------------------------------------------
