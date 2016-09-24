#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class Mouse(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Mouse Position"

    # ----------------------------------------------------------------------
    def generate_header(self):
        return ""

    # ----------------------------------------------------------------------
    def generate_vars(self):
        return """
// block_$id$ = Mouse
var block_$id$_o0 = [];
var block_$id$_o1 = [];
"""

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return """
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

    # ----------------------------------------------------------------------
    def generate_dealloc(self):
        return """"""


    # ----------------------------------------------------------------------
    def generate_out_dealloc(self):
        return ""

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Label": _("Mouse Position"),
            "Icon": "images/show.png",
            "Color": "50:50:50:150",
            "InTypes": {},
            "OutTypes": {0: "HRP_WEBAUDIO_FLOAT", 1: "HRP_WEBAUDIO_FLOAT"},
            "TreeGroup": _("Interface"),
            "IsSource": True
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {}

# ------------------------------------------------------------------------------
