#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the ChannelMerger class.
"""
from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class ChannelMerger(Plugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)

        self.language = "javascript"
        self.framework = "webaudio"
        self.help = "Channel Merger"
        self.label = "Channel Merger"
        self.color = "50:150:250:150"

        self.in_ports = [{"type":"harpia.extensions.javascript.ports.sound",
                "label":"Sound Input 1",
                "name":"sound_input_1"},
                {"type":"harpia.extensions.javascript.ports.sound",
                "label":"Sound Input 2",
                "name":"sound_input_2"}
                ]
        self.out_ports = [{"type":"harpia.extensions.javascript.ports.sound",
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
var $out_ports[sound_output]$ = block_$id$_obj.node;
var $in_ports[sound_input_1]$ = block_$id$_obj.node;
var $in_ports[sound_input_2]$ = block_$id$_obj.node;
"""
