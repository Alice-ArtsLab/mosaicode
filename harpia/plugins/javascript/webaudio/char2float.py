#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class Char2Float(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)
        self.float = 60
        self.char = 'a'

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "char to float"

    # ----------------------------------------------------------------------
    def generate_header(self):
        return ""

    # ----------------------------------------------------------------------
    def generate_vars(self):
        return """
// block_$id$ = Char 2 Float
var block_$id$_o0 = [];
var block_$id$_i = [];
block_$id$_i[0] = function(value){
    if (value != '$char$')
        return true;
    for (var i = 0; i < block_$id$_o0.length ; i++){
        block_$id$_o0[i]($float$);
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
            "Label": _("Char 2 Float"),
            "Icon": "images/show.png",
            "Color": "200:200:25:150",
            "InTypes": {0: "HRP_WEBAUDIO_CHAR"},
            "OutTypes": {0: "HRP_WEBAUDIO_FLOAT"},
            "Description": _("Char 2 Float"),
            "TreeGroup": _("Conversion")
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {"float":{"name": "Output float",
                    "type": HARPIA_FLOAT,
                    "value": self.float,
                    "lower":0,
                    "upper":20000,
                    "step":1
                    },
                "char":{"name": "Input Char",
                    "type": HARPIA_STRING,
                    "value": self.char
                    }
        }

# ------------------------------------------------------------------------------
