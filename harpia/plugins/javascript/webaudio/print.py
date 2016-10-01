#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class Print(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)
        self.label = "Label"
        self.value = 1

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Print value"

    # ----------------------------------------------------------------------
    def generate_header(self):
        return ""

    # ----------------------------------------------------------------------
    def generate_vars(self):
        return """
// block_$id$ = Print
var block_$id$_i = [];
block_$id$_i[0] = function(value){
    document.getElementById("block_$id$").innerHTML = value;
    return true;
    };
block_$id$_i[1] = function(value){
    document.getElementById("block_$id$").innerHTML = value;
    return true;
    };
"""

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return """
"""

    # ----------------------------------------------------------------------
    def generate_dealloc(self):
        return """
$label$ <span id="block_$id$">$value$</span><br>
"""

    # ----------------------------------------------------------------------
    def generate_out_dealloc(self):
        return ""

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Label": "Print",
            "Icon": "images/show.png",
            "Color": "50:10:250:150",
            "InTypes": {0: "HRP_WEBAUDIO_FLOAT", 1: "HRP_WEBAUDIO_CHAR"},
            "OutTypes": {},
            "TreeGroup": "Interface"
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {"label":{"name": "Label",
                    "type": HARPIA_STRING
                    }
            }

# ------------------------------------------------------------------------------
