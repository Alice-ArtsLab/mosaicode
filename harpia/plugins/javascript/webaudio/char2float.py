#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.javascript.webaudio.webaudioplugin import WebaudioPlugin

class Char2Float(WebaudioPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        WebaudioPlugin.__init__(self)
        self.float = 60
        self.char = 'a'
        self.help = "char to float"
        self.vars = """
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
        self.description = {"Label": "Char 2 Float",
            "Icon": "images/show.png",
            "Color": "200:200:25:150",
            "InTypes": {0: "HRP_WEBAUDIO_CHAR"},
            "OutTypes": {0: "HRP_WEBAUDIO_FLOAT"},
            "TreeGroup": "Conversion"
            }

        self.properties = {"float":{"name": "Output float",
                    "type": HARPIA_FLOAT,
                    "lower":0,
                    "upper":20000,
                    "step":1
                    },
                "char":{"name": "Input Char",
                    "type": HARPIA_STRING
                    }
                }
