#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class ADSR(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)
        self.a = 5
        self.d = 2
        self.s = 100
        self.r = 50
        self.g = 0.2

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "ADSR"

    # ----------------------------------------------------------------------
    def generate_header(self):
        return """
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

    # ----------------------------------------------------------------------
    def generate_vars(self):
        return """
// block_$id$ = ADSR
var block_$id$_obj = new Envelope(context, $a$, $d$, $s$, $r$, $g$);
var block_$id$ =  block_$id$_obj.node;
var block_$id$_i = [];
block_$id$_i[0] = block_$id$_obj.node;
block_$id$_i[1] = function(value){
    block_$id$_obj.play();
};
"""
    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return ""

    # ----------------------------------------------------------------------
    def generate_dealloc(self):
        return ""

    # ----------------------------------------------------------------------
    def generate_out_dealloc(self):
        return ""

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Label": _("ADSR"),
            "Icon": "images/show.png",
            "Color": "50:150:250:150",
            "InTypes": {0: "HRP_WEBAUDIO_SOUND", 1: "HRP_WEBAUDIO_FLOAT"},
            "OutTypes": {0: "HRP_WEBAUDIO_SOUND"},
            "TreeGroup": _("Sound")
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {"a":{"name": "Attack",
                    "type": HARPIA_FLOAT,
                    "value": self.a,
                    "lower":0,
                    "upper":10000,
                    "step":1
                    },
                "d":{"name": "Delay",
                            "type": HARPIA_FLOAT,
                            "value": self.d,
                            "lower":0,
                            "upper":10000,
                            "step":1
                            },
                "s":{"name": "Sustain",
                            "type": HARPIA_FLOAT,
                            "value": self.s,
                            "lower":0,
                            "upper":10000,
                            "step":1
                            },
                "r":{"name": "Release",
                            "type": HARPIA_FLOAT,
                            "value": self.r,
                            "lower":0,
                            "upper":10000,
                            "step":1
                            },
                "g":{"name": "Gain",
                            "type": HARPIA_FLOAT,
                            "value": self.g,
                            "lower":0,
                            "upper":10000,
                            "step":1
                            }
            }

# ------------------------------------------------------------------------------
