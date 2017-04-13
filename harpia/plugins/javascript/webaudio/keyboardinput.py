#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the KeyboardInput class.
"""
from harpia.GUI.fieldtypes import *
from harpia.plugins.javascript.webaudio.webaudioplugin import WebaudioPlugin


class KeyboardInput(WebaudioPlugin):

    # --------------------------------------------------------------------------
    def __init__(self):
        WebaudioPlugin.__init__(self)

        # Appearance
        self.help = "Keyboard Input"
        self.label = "Keyboard Input"
        self.color = "50:150:250:150"
        self.out_ports = [{"type":"HRP_WEBAUDIO_FLOAT",
                "label":"Float Output",
                "name":"float_output"},
                {"type":"HRP_WEBAUDIO_CHAR",
                "label":"Char Output",
                "name":"char_output"}
            ]
        self.group = "Interface"

        self.codes[1] = """
// block_$id$ = KeyBoard Input
var block_$id$_o0 = [];
var block_$id$_o1 = [];
"""
        self.codes[2] = """
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
