#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class ChannelMerger(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Channel Merger"

    # ----------------------------------------------------------------------
    def generate_header(self):
        return """
Merger = function(context) {
  var that = this;
  this.x = 0; // Initial sample number
  this.context = context;
  this.node = context.createScriptProcessor(1024, 1, 1);
  this.node.onaudioprocess = function(e) { that.process(e) };
}

Merger.prototype.process = function(e) {
  var in1 = e.inputBuffer.getChannelData(0);
  var out = e.outputBuffer.getChannelData(0);
  for (var i = 0; i < in1.length; ++i) {
      out[i] = in1[i];
  }
}
"""
    # ----------------------------------------------------------------------
    def generate_vars(self):
        return """
// block_$id$ = Channel Merger
var block_$id$_obj = new Merger(context);
var block_$id$ = block_$id$_obj.node;
var block_$id$_i = [];
block_$id$_i[0] = block_$id$_obj.node;
block_$id$_i[1] = block_$id$_obj.node;
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
        return {"Type": str(self.type),
            "Label": _("Channel Merger"),
            "Icon": "images/show.png",
            "Color": "50:150:250:150",
            "InTypes": {0: "HRP_WEBAUDIO_SOUND", 1: "HRP_WEBAUDIO_SOUND"},
            "OutTypes": {0: "HRP_WEBAUDIO_SOUND"},
            "Description": _("Channel Merger"),
            "TreeGroup": _("Sound"),
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {}

# ------------------------------------------------------------------------------
