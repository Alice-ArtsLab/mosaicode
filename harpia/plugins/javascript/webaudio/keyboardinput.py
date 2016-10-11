#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.javascript.webaudio.webaudioplugin import WebaudioPlugin

class KeyboardInput(WebaudioPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        WebaudioPlugin.__init__(self)
        self.help = "Keyboard Input"
        self.vars = """
// block_$id$ = KeyBoard Input
var block_$id$_o0 = [];
var block_$id$_o1 = [];
"""
        self.function_call = """
document.onkeypress = function(evt){
    evt = evt || window.event;
    var value = evt.keyCode || evt.which;
    for (var i = 0; i < block_$id$_o0.length ; i++){
        block_$id$_o0[i](value);
    }
    value = String.fromCharCode(value);
    for (var i = 0; i < block_$id$_o1.length ; i++){
        block_$id$_o1[i](value);
    }
};
"""
        self.description = {"Label": "Keyboard Input",
            "Icon": "images/show.png",
            "Color": "50:150:20:150",
            "InTypes": {},
            "OutTypes": {0: "HRP_WEBAUDIO_FLOAT", 1: "HRP_WEBAUDIO_CHAR"},
            "TreeGroup": "Interface"
            }
