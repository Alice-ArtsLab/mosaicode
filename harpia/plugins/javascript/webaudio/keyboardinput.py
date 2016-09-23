#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class KeyboardInput(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)
        self.id = -1
        self.type = self.__class__.__module__

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Keyboard Input"

    # ----------------------------------------------------------------------
    def generate_header(self):
        return ""

    # ----------------------------------------------------------------------
    def generate_vars(self):
        return """
var block_$id$_o1 = [];
var block_$id$_o2 = [];
"""

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return """
document.onkeypress = function(evt){
    evt = evt || window.event;
    var value = evt.keyCode || evt.which;
    for (var i = 0; i < block_$id$_o1.length ; i++){
        block_$id$_o1[i](value);
    }
    value = String.fromCharCode(value);
    for (var i = 0; i < block_$id$_o2.length ; i++){
        block_$id$_o2[i](value);
    }
};
"""

    # ----------------------------------------------------------------------
    def generate_dealloc(self):
        return """
"""


    # ----------------------------------------------------------------------
    def generate_out_dealloc(self):
        return ""

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            "Label": _("Keyboard Input"),
            "Icon": "images/show.png",
            "Color": "50:150:20:150",
            "InTypes": {},
            "OutTypes": {0: "HRP_WEBAUDIO_FLOAT", 1: "HRP_WEBAUDIO_CHAR"},
            "Description": _("Keyboard Input"),
            "TreeGroup": _("Interface")
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {}

# ------------------------------------------------------------------------------
