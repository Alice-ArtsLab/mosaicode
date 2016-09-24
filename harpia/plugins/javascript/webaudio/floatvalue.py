#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class FloatValue(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)
        self.value = 1
        self.label = "Label"
        self.min = 0
        self.max = 10

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Double value"

    # ----------------------------------------------------------------------
    def generate_header(self):
        return ""

    # ----------------------------------------------------------------------
    def generate_vars(self):
        return """
// block_$id$ = Float Value
var block_$id$_value = $value$;
var block_$id$_o0 = [];
"""

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return """
function change_$id$_value(){
    value = document.getElementById("block_$id$").value;
    for (var i = 0; i < block_$id$_o0.length ; i++){
        block_$id$_o0[i](value);
    }
};
"""

    # ----------------------------------------------------------------------
    def generate_dealloc(self):
        return """
$label$ <input type="number" id="block_$id$" value="$value$" min="$min$" max="$max$" onChange="change_$id$_value();"><br>
"""


    # ----------------------------------------------------------------------
    def generate_out_dealloc(self):
        return ""

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Label": _("FloatValue"),
            "Icon": "images/show.png",
            "Color": "50:150:20:150",
            "InTypes": {},
            "OutTypes": {0: "HRP_WEBAUDIO_FLOAT"},
            "TreeGroup": _("Interface")
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {"value":{"name": "Value",
                    "type": HARPIA_FLOAT,
                    "value": self.value,
                    "lower":0,
                    "upper":20000,
                    "step":1
                    },
                "min":{"name": "Min",
                    "type": HARPIA_FLOAT,
                    "value": self.min,
                    "lower":0,
                    "upper":20000,
                    "step":1
                    },
                "max":{"name": "Max",
                    "type": HARPIA_FLOAT,
                    "value": self.max,
                    "lower":00,
                    "upper":20000,
                    "step":1
                    },
                "label":{"name": "Label",
                    "type": HARPIA_STRING,
                    "value": self.label
                    }
            }

# ------------------------------------------------------------------------------
