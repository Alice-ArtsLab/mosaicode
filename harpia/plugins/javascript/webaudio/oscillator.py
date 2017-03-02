#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Oscillator class.
"""
from harpia.GUI.fieldtypes import *
from harpia.plugins.javascript.webaudio.webaudioplugin import WebaudioPlugin


class Oscillator(WebaudioPlugin):

    # --------------------------------------------------------------------------
    def __init__(self):
        WebaudioPlugin.__init__(self)

        # Appearance
        self.help = "Sound output"
        self.label = "Oscillator"
        self.color = "50:150:250:150"
        self.in_ports = [{"type":"HRP_WEBAUDIO_SOUND",
                           "label":"Osc Frequency",
                           "name":"osc_freq"},
                         {"type":"HRP_WEBAUDIO_FLOAT",
                         "label":"Frequency",
                         "name":"freq"},
                         {"type":"HRP_WEBAUDIO_FLOAT",
                         "name":"detune",
                         "label":"Detune"}]
        self.out_ports = [{"type":"HRP_WEBAUDIO_SOUND",
                         "name":"sound_output",
                         "label":"Sound Output"}]
        self.group = "Sound"

        self.properties = [{"name": "freq",
                            "label": "Frequency",
                            "type": HARPIA_FLOAT,
                            "lower": 20,
                            "upper": 20000,
                            "step": 1,
                            "value": 440
                            },
                           {"name": "oscillator_type",
                            "label": "Type",
                            "type": HARPIA_COMBO,
                            "values": ["square",
                                       "sine",
                                       "sawtooth",
                                       "triangle"],
                            "value": "sine"
                            }
                           ]

        self.vars = """
// block_$id$ = Oscillator
var block_$id$ =  context.createOscillator();
var block_$id$_i = [];
block_$id$_i[0] = block_$id$.frequency;
block_$id$_i[1] = function(value){
    block_$id$.frequency.value = value;
};
block_$id$_i[2] = function(value){
    oscillator = ''
    if (value < 1) oscillator = 'square';
    if (value == 1) oscillator = 'sine';
    if (value == 2) oscillator = 'sawtooth';
    if (value > 2) oscillator = 'triangle';
    block_$id$.type = oscillator;
};
"""
        self.function_call = """
block_$id$.type = '$oscillator_type$';
block_$id$.frequency.value = $freq$; // value in hertz
block_$id$.detune.value = 100; // value in cents
block_$id$.start(0);
"""
