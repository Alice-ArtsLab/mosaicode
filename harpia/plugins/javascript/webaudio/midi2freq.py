#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.javascript.webaudio.webaudioplugin import WebaudioPlugin

class Midi2Freq(WebaudioPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        WebaudioPlugin.__init__(self)
        self.help = "midi to freq"
        self.vars = """
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
        self.description = {"Label": "Midi 2 Freq",
            "Icon": "images/show.png",
            "Color": "200:200:25:150",
            "InTypes": {0: "HRP_WEBAUDIO_FLOAT"},
            "OutTypes": {0: "HRP_WEBAUDIO_FLOAT"},
            "TreeGroup": "Conversion"
            }
