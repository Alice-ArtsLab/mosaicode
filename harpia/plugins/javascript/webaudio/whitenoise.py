#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class WhiteNoise(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "White Noise"

    # ----------------------------------------------------------------------
    def generate_header(self):
        return """
WhiteNoise = function(context) {
  var that = this;
  this.x = 0; // Initial sample number
  this.context = context;
  this.node = context.createScriptProcessor(1024, 0, 2);
  this.node.onaudioprocess = function(e) { that.process(e) };
}

WhiteNoise.prototype.process = function(e) {
  var data_l = e.outputBuffer.getChannelData(0);
  var data_r = e.outputBuffer.getChannelData(1);
  for (var i = 0; i < data_l.length; ++i) {
//    data[i] = Math.sin(this.x++);
      data_l[i] = (Math.random() * 2) - 1;
      data_r[i] = (Math.random() * 2) - 1;
  }
}
"""
    # ----------------------------------------------------------------------
    def generate_vars(self):
        return """
// block_$id$ = White Noise
var block_$id$ =  new WhiteNoise(context).node;
"""

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return """
"""

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
        return {"Label": _("White Noise"),
            "Icon": "images/show.png",
            "Color": "50:150:250:150",
            "InTypes": {},
            "OutTypes": {0: "HRP_WEBAUDIO_SOUND"},
            "TreeGroup": _("Sound")
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {}

# ------------------------------------------------------------------------------
