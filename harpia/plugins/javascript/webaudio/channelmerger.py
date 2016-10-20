#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.javascript.webaudio.webaudioplugin import WebaudioPlugin


class ChannelMerger(WebaudioPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        WebaudioPlugin.__init__(self)

        self.help = "Channel Merger"
        self.header = """
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
        self.vars = """
// block_$id$ = Channel Merger
var block_$id$_obj = new Merger(context);
var block_$id$ = block_$id$_obj.node;
var block_$id$_i = [];
block_$id$_i[0] = block_$id$_obj.node;
block_$id$_i[1] = block_$id$_obj.node;
"""
        self.description = {"Label": "Channel Merger",
                            "Icon": "images/show.png",
                            "Color": "50:150:250:150",
                            "InTypes": {0: "HRP_WEBAUDIO_SOUND",
                                        1: "HRP_WEBAUDIO_SOUND"},
                            "OutTypes": {0: "HRP_WEBAUDIO_SOUND"},
                            "TreeGroup": "Sound",
                            }
