#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Mouse class.
"""
from harpia.GUI.fieldtypes import *
from harpia.plugins.javascript.webaudio.webaudioplugin import WebaudioPlugin


class Mouse(WebaudioPlugin):

    # --------------------------------------------------------------------------
    def __init__(self):
        WebaudioPlugin.__init__(self)

        # Appearance
        self.help = "Mouse Position"
        self.label = "Mouse Position"
        self.icon = "images/show.png"
        self.color = "50:50:50:150"
        self.out_types = ["HRP_WEBAUDIO_FLOAT", "HRP_WEBAUDIO_FLOAT"]
        self.group = "Interface"

        self.vars = """
// block_$id$ = Mouse
var block_$id$_o0 = [];
var block_$id$_o1 = [];
"""
        self.function_call = """
// ----------------- Mouse position ----------------------------
// Detect if the browser is IE or not.
// If it is not IE, we assume that the browser is NS.
var IE = document.all?true:false

// If NS -- that is, !IE -- then set up for mouse capture
if (!IE) document.captureEvents(Event.MOUSEMOVE)

// Set-up to use getMouseXY function onMouseMove
document.onmousemove = getMouseXY;

// Temporary variables to hold mouse x-y pos.s
var tempX = 0
var tempY = 0

// Main function to retrieve mouse x-y pos.s

function getMouseXY(e) {
  if (IE) { // grab the x-y pos.s if browser is IE
    tempX = event.clientX + document.body.scrollLeft
    tempY = event.clientY + document.body.scrollTop
  } else {  // grab the x-y pos.s if browser is NS
    tempX = e.pageX
    tempY = e.pageY
  }
  // catch possible negative values in NS4
  if (tempX < 0){tempX = 0}
  if (tempY < 0){tempY = 0}

    // X value
    for (var i = 0; i < block_$id$_o0.length ; i++)
        block_$id$_o0[i](tempX);

    // Y value
    for (var i = 0; i < block_$id$_o1.length ; i++)
        block_$id$_o1[i](tempY);
  return true
}
// ----------------- Mouse position ----------------------------
"""
