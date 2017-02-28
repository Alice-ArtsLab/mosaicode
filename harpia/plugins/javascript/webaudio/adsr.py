#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the ADSR class.
"""
from harpia.GUI.fieldtypes import *
from harpia.plugins.javascript.webaudio.webaudioplugin import WebaudioPlugin


class ADSR(WebaudioPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        WebaudioPlugin.__init__(self)

        # Appearance
        self.help = "ADSR"
        self.label = "ADSR"
        self.color = "50:150:250:150"
        self.in_types = ["HRP_WEBAUDIO_SOUND", "HRP_WEBAUDIO_FLOAT"]
        self.out_types = ["HRP_WEBAUDIO_SOUND"]
        self.group = "Sound"

        self.header = """
Envelope = function(context, a, d, s, r, g) {
this.node = context.createGain()
this.context = context;
this.node.gain.value = 0;
this.a = a / 1000.0;
this.d = d / 1000.0;
this.s = s / 1000.0;
this.r = r / 1000.0;
this.g = g;
}

Envelope.prototype.play = function(e) {
var time = this.context.currentTime;
// Zero
this.node.gain.linearRampToValueAtTime(0, time);
// Attack time
time += this.a;
this.node.gain.linearRampToValueAtTime(1, time);
// Decay time
time += this.d;
this.node.gain.linearRampToValueAtTime(0.5, time);
// Sustain time (do nothing)
time += this.s;
// Release time
time += this.r;
this.node.gain.linearRampToValueAtTime(0, time);
}
"""
        self.vars = """
// block_$id$ = ADSR
var block_$id$_obj = new Envelope(context, $a$, $d$, $s$, $r$, $g$);
var block_$id$ =  block_$id$_obj.node;
var block_$id$_i = [];
block_$id$_i[0] = block_$id$_obj.node;
block_$id$_i[1] = function(value){
    block_$id$_obj.play();
};
"""
        self.properties = [
            {"name": "a",
             "label": "Attack",
             "type": HARPIA_FLOAT,
             "lower": 0,
             "upper": 10000,
             "step": 1,
             "value": 5
             },
            {"name": "d",
             "label": "Delay",
             "type": HARPIA_FLOAT,
             "lower": 0,
             "upper": 10000,
             "step": 1,
             "value": 2
             },
            {"name": "s",
             "label": "Sustain",
             "type": HARPIA_FLOAT,
             "lower": 0,
             "upper": 10000,
             "step": 1,
             "value": 100
             },
            {"name": "r",
             "label": "Release",
             "type": HARPIA_FLOAT,
             "lower": 0,
             "upper": 10000,
             "step": 1,
             "value": 50
             },
            {"name": "g",
             "label": "Gain",
             "type": HARPIA_FLOAT,
             "lower": 0,
             "upper": 10000,
             "step": 1,
             "value": 0.5
             }
        ]
