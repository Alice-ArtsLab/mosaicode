#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.javascript.webaudio.webaudioplugin import WebaudioPlugin


class Button(WebaudioPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        WebaudioPlugin.__init__(self)
        self.value = 1
        self.label = "Label"
        self.help = "Button"
        self.vars = """
// block_$id$ = Button
var block_$id$_value = $value$;
var block_$id$_o0 = [];
"""

        self.function_call = """
function click_$id$(){
    value = document.getElementById("block_$id$").value;
    for (var i = 0; i < block_$id$_o0.length ; i++){
        block_$id$_o0[i](value);
    }
};
"""

        self.dealloc = """
<button type="button" value="$value$" onClick="click_$id$();"
id="block_$id$">$label$</button><br>
"""

        self.description = {"Label": "Button",
                            "Icon": "images/show.png",
                            "Color": "50:150:20:150",
                            "InTypes": {},
                            "OutTypes": {0: "HRP_WEBAUDIO_FLOAT"},
                            "TreeGroup": "Interface"
                            }

        self.properties = {"value": {"name": "Value",
                                     "type": HARPIA_FLOAT,
                                     "lower": 0,
                                     "upper": 20000,
                                     "step": 1
                                     },
                           "label": {"name": "Label",
                                     "type": HARPIA_STRING
                                     }
                           }
