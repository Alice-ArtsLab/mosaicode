#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Print class.
"""
from harpia.GUI.fieldtypes import *
from harpia.plugins.javascript.webaudio.webaudioplugin import WebaudioPlugin


class Print(WebaudioPlugin):

    # --------------------------------------------------------------------------
    def __init__(self):
        WebaudioPlugin.__init__(self)

        # Appearance
        self.help = "Print value"
        self.label = "Print"
        self.color = "50:150:250:150"
        self.in_ports = [{"type":"HRP_WEBAUDIO_FLOAT",
                "name":"float_value",
                "label":"Float Value"},
                {"type":"HRP_WEBAUDIO_CHAR",
                "name":"Char Value",
                "label":"char_value"}
                ]
        self.group = "Interface"

        self.vars = """
// block_$id$ = $name$
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
$label$ <span id="block_$id$"></span><br>
"""
        self.properties = [{"name": "label",
                            "label": "Label",
                            "value": "Label",
                            "type": HARPIA_STRING
                            }
                           ]
