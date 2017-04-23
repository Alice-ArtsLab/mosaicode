#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the DivideFloat class.
"""
from harpia.GUI.fieldtypes import *
from harpia.plugins.javascript.webaudio.webaudioplugin import WebaudioPlugin


class DivideFloat(WebaudioPlugin):

    # ------------------------------------------------------------------------------
    def __init__(self):
        WebaudioPlugin.__init__(self)

        # Appearance
        self.help = "Divide Float"
        self.label = "Divide Float"
        self.color = "200:200:25:150"
        self.in_ports = [{"type":"HRP_WEBAUDIO_FLOAT",
                "name":"first_number",
                "label":"First Number"},
                {"type":"HRP_WEBAUDIO_FLOAT",
                "name":"second_number",
                "label":"Second Number"}
                ]
        self.out_ports = [{"type":"HRP_WEBAUDIO_FLOAT",
                "label":"Result",
                "name":"result"}
            ]
        self.group = "Arithmetics"

        self.codes[1] = """

// block_$id$ = Divide Float
var block_$id$_arg1 = 0;
var block_$id$_arg2 = 0;
var $out_ports[result]$ = [];

var $in_ports[first_number]$ = function(value){
    block_$id$_arg1 = parseFloat(value);
    block_$id$_arg2 = (parseFloat(block_$id$_arg2) == 0) ?
            1 : parseFloat(block_$id$_arg2);
    result = parseFloat(block_$id$_arg1) / parseFloat(block_$id$_arg2);
    for (var i = 0; i < $out_ports[result]$.length ; i++){
        $out_ports[result]$[i](result);
    }
    return true;
    };

var $in_ports[second_number]$ = function(value){
    block_$id$_arg2 = parseFloat(value);
    block_$id$_arg2 = (parseFloat(block_$id$_arg2) == 0) ?
            1 : parseFloat(block_$id$_arg2);
    result = parseFloat(block_$id$_arg1) / parseFloat(block_$id$_arg2);
    for (var i = 0; i < $out_ports[result]$.length ; i++){
        $out_ports[result]$[i](result);
    }
    return true;
    };
"""
