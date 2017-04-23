#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Midi2Freq class.
"""
from harpia.GUI.fieldtypes import *
from harpia.plugins.javascript.webaudio.webaudioplugin import WebaudioPlugin


class Midi2Freq(WebaudioPlugin):

    # --------------------------------------------------------------------------
    def __init__(self):
        WebaudioPlugin.__init__(self)

        # Appearance
        self.help = "midi to freq"
        self.label = "Midi 2 Freq"
        self.color = "200:200:25:150"
        self.in_ports = [{"type":"HRP_WEBAUDIO_FLOAT",
                "name":"midi_value",
                "label":"Midi Value"}
                ]
        self.out_ports = [{"type":"HRP_WEBAUDIO_FLOAT",
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
