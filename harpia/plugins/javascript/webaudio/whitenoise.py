#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the WhiteNoise class.
"""
from harpia.GUI.fieldtypes import *
from harpia.plugins.javascript.webaudio.webaudioplugin import WebaudioPlugin


class WhiteNoise(WebaudioPlugin):

    # --------------------------------------------------------------------------
    def __init__(self):
        WebaudioPlugin.__init__(self)

        # Appearance
        self.help = "White Noise"
        self.label = "White Noise"
        self.color = "50:150:250:150"
        self.out_ports = [{"type":"HRP_WEBAUDIO_SOUND",
                "label":"Sound Output",
                "name":"sound_output"}
            ]
        self.group = "Sound"

        self.codes[0] = """
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
        self.codes[1] = """
// block_$id$ = $label$
var block_$id$ =  new WhiteNoise(context);
var block_$id$_o0 = null;
"""

        self.codes[2] = "block_$id$_o0 = block_$id$.node;\n"
