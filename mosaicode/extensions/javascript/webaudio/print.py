#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Print class.
"""
from mosaicode.GUI.fieldtypes import *
from mosaicode.model.plugin import Plugin

class Print(Plugin):

    # --------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)

        self.language = "javascript"
        self.framework = "webaudio"
        self.help = "Print value"
        self.label = "Print"
        self.color = "50:150:250:150"
        self.in_ports = [{"type":"mosaicode.extensions.javascript.ports.float",
                "name":"float_value",
                "label":"Float Value"},
                {"type":"mosaicode.extensions.javascript.ports.char",
                "name":"Char Value",
                "label":"char_value"}
                ]
        self.group = "Interface"

        self.properties = [{"name": "label",
                            "label": "Label",
                            "value": "Label",
                            "type": MOSAICODE_STRING
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
