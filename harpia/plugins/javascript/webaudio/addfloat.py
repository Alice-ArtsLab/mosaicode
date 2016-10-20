#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.javascript.webaudio.webaudioplugin import WebaudioPlugin


class AddFloat(WebaudioPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        WebaudioPlugin.__init__(self)
        self.help = "Add Float"
        self.description = {"Label": "Add Float",
                            "Icon": "images/dilate.png",
                            "Color": "200:200:25:150",
                            "InTypes": {0: "HRP_WEBAUDIO_FLOAT",
                                        1: "HRP_WEBAUDIO_FLOAT"},
                            "OutTypes": {0: "HRP_WEBAUDIO_FLOAT"},
                            "TreeGroup": "Arithmetics"
                            }

        self.vars = """
// block_$id$ = Add Float
var block_$id$_arg1 = 0;
var block_$id$_arg2 = 0;
var block_$id$_o0 = [];
var block_$id$_i = []; //

block_$id$_i[0] = function(value){
    block_$id$_arg1 = parseFloat(value);
    result = parseFloat(block_$id$_arg1) + parseFloat(block_$id$_arg2);
    for (var i = 0; i < block_$id$_o0.length ; i++){
        block_$id$_o0[i](result);
    }
    return true;
    };
block_$id$_i[1] = function(value){
    block_$id$_arg2 = parseFloat(value);
    result = parseFloat(block_$id$_arg1) + parseFloat(block_$id$_arg2);
    for (var i = 0; i < block_$id$_o0.length ; i++){
        block_$id$_o0[i](result);
    }
    return true;
    };
"""
