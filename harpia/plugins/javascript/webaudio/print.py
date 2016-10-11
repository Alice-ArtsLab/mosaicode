#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.javascript.webaudio.webaudioplugin import WebaudioPlugin

class Print(WebaudioPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        WebaudioPlugin.__init__(self)
        self.label = "Label"
        self.value = 1
        self.help = "Print value"
        self.vars = """
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
        self.dealloc = """
$label$ <span id="block_$id$">$value$</span><br>
"""
        self.description = {"Label": "Print",
            "Icon": "images/show.png",
            "Color": "50:10:250:150",
            "InTypes": {0: "HRP_WEBAUDIO_FLOAT", 1: "HRP_WEBAUDIO_CHAR"},
            "OutTypes": {},
            "TreeGroup": "Interface"
            }

        self.properties = {"label":{"name": "Label",
                    "type": HARPIA_STRING
                    }
            }
