#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the ChannelMerger class.
"""
from harpia.GUI.fieldtypes import *
from harpia.plugins.javascript.webaudio.webaudioplugin import WebaudioPlugin


class ChannelMerger(WebaudioPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        WebaudioPlugin.__init__(self)

        # Appearance
        self.help = "Channel Merger"
        self.label = "Channel Merger"
        self.color = "50:150:250:150"

        self.in_ports = [{"type":"HRP_WEBAUDIO_SOUND",
                "label":"Sound Input 1",
                "name":"sound_input_1"},
                {"type":"HRP_WEBAUDIO_SOUND",
                "label":"Sound Input 2",
                "name":"sound_input_2"}
                ]
        self.out_ports = [{"type":"HRP_WEBAUDIO_SOUND",
                "label":"Sound Output",
                "name":"sound_output"}
            ]

        self.group = "Sound"

        self.codes[0] = """
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
        self.codes[1] = """
// block_$id$ = Channel Merger
var block_$id$_obj = new Merger(context);
var block_$id$ = block_$id$_obj.node;
var block_$id$_i0 = block_$id$_obj.node;
var block_$id$_i1 = block_$id$_obj.node;
"""
