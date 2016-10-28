#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.javascript.webaudio.webaudioplugin import WebaudioPlugin


class Print(WebaudioPlugin):

    # --------------------------------------------------------------------------
    def __init__(self):
        WebaudioPlugin.__init__(self)

        # Appearance
        self.help = "Print value"
        self.label = "Print"
        self.icon = "images/show.png"
        self.color = "50:150:250:150"
        self.in_types = ["HRP_WEBAUDIO_FLOAT", "HRP_WEBAUDIO_CHAR"]
        self.group = "Interface"

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
$label$ <span id="block_$id$"></span><br>
"""
        self.properties = [{"name": "label",
                            "label" : "Label",
                            "value" : "Label",
                            "type": HARPIA_STRING
                                     }
                           ]
