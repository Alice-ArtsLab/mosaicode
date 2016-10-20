#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.javascript.webaudio.webaudioplugin import WebaudioPlugin


class Oscillator(WebaudioPlugin):

    # --------------------------------------------------------------------------
    def __init__(self):
        WebaudioPlugin.__init__(self)
        self.freq = 440
        self.oscillator_type = 'sine'
        self.help = "Sound output"
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
        self.description = {"Label": "Oscillator",
                            "Icon": "images/show.png",
                            "Color": "50:150:250:150",
                            "InTypes": {0: "HRP_WEBAUDIO_SOUND",
                                        1: "HRP_WEBAUDIO_FLOAT",
                                        2: "HRP_WEBAUDIO_FLOAT"},
                            "OutTypes": {0: "HRP_WEBAUDIO_SOUND"},
                            "TreeGroup": "Sound"
                            }

        self.properties = {"freq": {"name": "Frequency",
                                    "type": HARPIA_FLOAT,
                                    "lower": 20,
                                    "upper": 20000,
                                    "step": 1
                                    },
                           "oscillator_type": {"name": "Type",
                                               "type": HARPIA_COMBO,
                                               "values": ["square", "sine",
                                                          "sawtooth",
                                                          "triangle"]
                                               }
                           }
