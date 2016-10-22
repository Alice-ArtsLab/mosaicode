#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.javascript.webaudio.webaudioplugin import WebaudioPlugin


class WhiteNoise(WebaudioPlugin):

    # --------------------------------------------------------------------------
    def __init__(self):
        WebaudioPlugin.__init__(self)

        # Appearance
        self.help = "White Noise"
        self.label = "White Noise"
        self.icon = "images/show.png"
        self.color = "50:150:250:150"
        self.out_types = ["HRP_WEBAUDIO_SOUND"]
        self.group = "Sound"

        self.header = """
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
        self.vars = """
// block_$id$ = White Noise
var block_$id$ =  new WhiteNoise(context).node;
"""
