#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Midi2Freq class.
"""
from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class Midi2Freq(Plugin):

    # --------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)

        self.language = "javascript"
        self.framework = "webaudio"
        self.help = "midi to freq"
        self.label = "Midi 2 Freq"
        self.color = "200:200:25:150"
        self.in_ports = [{"type":"harpia.extensions.javascript.ports.float",
                "name":"midi_value",
                "label":"Midi Value"}
                ]
        self.out_ports = [{"type":"harpia.extensions.javascript.ports.float",
                "label":"Frequency",
                "name":"frequency"}
            ]
        self.group = "Conversion"
        self.codes[1] = """
// block_$id$ = $label$
var $out_ports[frequency]$ = [];

var $in_ports[midi_value]$ = function(value){
    value = (value < 0) ? 0 : value;
    value = (value >127) ? 127 : value;
    var arg = ((parseFloat(value) - 69.0) / 12.0);
    result =  Math.pow(2.0, arg) * 440.0;
    for (var i = 0; i < $out_ports[frequency]$.length ; i++){
        $out_ports[frequency]$[i](result);
    }
    return true;
    };
"""
