#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the AddFloat class.
"""
from harpia.GUI.fieldtypes import *
from harpia.plugins.javascript.webaudio.webaudioplugin import WebaudioPlugin


class AddFloat(WebaudioPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        WebaudioPlugin.__init__(self)

        # Appearance
        self.help = "Add Float"
        self.label = "Add Float"
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

        self.vars = """
// block_$id$ = Add Float
var block_$id$_arg1 = 0;
var block_$id$_arg2 = 0;
var block_$id$_o0 = [];

var block_$id$_i0 = function(value){
    block_$id$_arg1 = parseFloat(value);
    result = parseFloat(block_$id$_arg1) + parseFloat(block_$id$_arg2);
    for (var i = 0; i < block_$id$_o0.length ; i++){
        block_$id$_o0[i](result);
    }
    return true;
    };

var block_$id$_i1 = function(value){
    block_$id$_arg2 = parseFloat(value);
    result = parseFloat(block_$id$_arg1) + parseFloat(block_$id$_arg2);
    for (var i = 0; i < block_$id$_o0.length ; i++){
        block_$id$_o0[i](result);
    }
    return true;
    };
"""
