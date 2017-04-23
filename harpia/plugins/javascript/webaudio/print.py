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

        self.properties = [{"name": "label",
                            "label": "Label",
                            "value": "Label",
                            "type": HARPIA_STRING
                            }
                           ]

        self.codes[1] = """
// block_$id$ = $name$
var $in_ports[float_value]$ = function(value){
    document.getElementById("block_$id$").innerHTML = value;
    return true;
    };
var $in_ports[char_value]$ = $in_ports[result]$;
"""
        self.codes[3] = """
$prop[label]$ <span id="block_$id$"></span><br>
"""
