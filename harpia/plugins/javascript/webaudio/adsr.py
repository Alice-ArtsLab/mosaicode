#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.javascript.webaudio.webaudioplugin import WebaudioPlugin


class ADSR(WebaudioPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        WebaudioPlugin.__init__(self)
        self.a = 5
        self.d = 2
        self.s = 100
        self.r = 50
        self.g = 0.2
        self.help = "ADSR"
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
        self.description = {
            "Label": "ADSR",
            "Icon": "images/show.png",
            "Color": "50:150:250:150",
            "InTypes": {0: "HRP_WEBAUDIO_SOUND", 1: "HRP_WEBAUDIO_FLOAT"},
            "OutTypes": {0: "HRP_WEBAUDIO_SOUND"},
            "TreeGroup": "Sound"
        }

        self.properties = {
            "a": {"name": "Attack",
                  "type": HARPIA_FLOAT,
                  "lower": 0,
                  "upper": 10000,
                  "step": 1
                  },
            "d": {"name": "Delay",
                  "type": HARPIA_FLOAT,
                  "lower": 0,
                  "upper": 10000,
                  "step": 1
                  },
            "s": {"name": "Sustain",
                  "type": HARPIA_FLOAT,
                  "lower": 0,
                  "upper": 10000,
                  "step": 1
                  },
            "r": {"name": "Release",
                  "type": HARPIA_FLOAT,
                  "lower": 0,
                  "upper": 10000,
                  "step": 1
                  },
            "g": {"name": "Gain",
                  "type": HARPIA_FLOAT,
                  "lower": 0,
                  "upper": 10000,
                  "step": 1
                  }
        }
