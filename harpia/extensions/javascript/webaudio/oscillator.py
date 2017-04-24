#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Oscillator class.
"""
from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class Oscillator(Plugin):

    # --------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)

        self.language = "javascript"
        self.framework = "webaudio"
        self.help = "Sound output"
        self.label = "Oscillator"
        self.color = "50:150:250:150"
        self.in_ports = [{"type":"harpia.extensions.javascript.ports.sound",
                           "label":"Osc Frequency",
                           "name":"osc_freq"},
                         {"type":"harpia.extensions.javascript.ports.float",
                         "label":"Frequency",
                         "name":"freq"},
                         {"type":"harpia.extensions.javascript.ports.float",
                         "name":"type",
                         "label":"Type"}]
        self.out_ports = [{"type":"harpia.extensions.javascript.ports.sound",
                         "name":"sound",
                         "label":"Sound"}]
        self.group = "Sound"

        self.properties = [{"name": "freq",
                            "label": "Frequency",
                            "type": HARPIA_FLOAT,
                            "lower": 0,
                            "step": 1,
                            "value": 440
                            },
                           {"name": "type",
                            "label": "Type",
                            "type": HARPIA_COMBO,
                            "values": ["square",
                                       "sine",
                                       "sawtooth",
                                       "triangle"],
                            "value": "sine"
                            }
                           ]

        self.codes[0] = """
// block_$id$ = Oscillator
var block_$id$ =  context.createOscillator();
var $in_ports[osc_freq]$ = block_$id$.frequency;
var $out_ports[sound]$ = null;
var $in_ports[freq]$ = function(value){
    block_$id$.frequency.value = value;
};
var $in_ports[type]$ = function(value){
    oscillator = ''
    if (value < 1) oscillator = 'square';
    if (value == 1) oscillator = 'sine';
    if (value == 2) oscillator = 'sawtooth';
    if (value > 2) oscillator = 'triangle';
    block_$id$.type = oscillator;
};
"""
        self.codes[1] = """
$out_ports[sound]$ = block_$id$.frequency;
block_$id$.type = '$prop[type]$';
block_$id$.frequency.value = $prop[freq]$; // value in hertz
block_$id$.detune.value = 100; // value in cents
block_$id$.start(0);
"""
