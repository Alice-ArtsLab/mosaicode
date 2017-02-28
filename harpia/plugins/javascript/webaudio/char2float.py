#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Char2Float class.
"""
from harpia.GUI.fieldtypes import *
from harpia.plugins.javascript.webaudio.webaudioplugin import WebaudioPlugin


class Char2Float(WebaudioPlugin):

    # --------------------------------------------------------------------------
    def __init__(self):
        WebaudioPlugin.__init__(self)

        # Appearance
        self.help = "Char to Float"
        self.label = "Char 2 Float"
        self.color = "200:200:25:150"
        self.in_types = ["HRP_WEBAUDIO_CHAR"]
        self.out_types = ["HRP_WEBAUDIO_FLOAT"]
        self.group = "Conversion"

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

        self.properties = [{"name": "float",
                            "label": "Output float",
                                     "type": HARPIA_FLOAT,
                                     "lower": 0,
                                     "upper": 20000,
                                     "step": 1,
                                     "value": 60
                            },
                           {"name": "char",
                            "label": "Input Char",
                            "type": HARPIA_STRING,
                            "value": "a"
                            }
                           ]
