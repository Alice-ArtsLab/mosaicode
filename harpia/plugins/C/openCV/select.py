#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin

class Select(OpenCVPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.key = " "

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Select between two images"

    # ----------------------------------------------------------------------
    def generate_vars(self):
        return OpenCVPlugin.generate_vars(self) + 'char block$id$_key = \'$key$\';\n'

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return 'if(block$id$_img_i0 && block$id$_img_i1){\n' + \
            'if (key != -1)\n' + \
            'block$id$_key = key;\n' + \
            'if (block$id$_key == \'$key$\' )\n' + \
            'block$id$_img_o0 = cvCloneImage(block$id$_img_i0);\n' + \
            'else\n' + \
            'block$id$_img_o0 = cvCloneImage(block$id$_img_i1);\n' + \
            'printf("%c\\n", key);\n' + \
            '}\n'

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Label": "Select",
            "Icon": "images/show.png",
            "Color": "50:100:200:150",
            "InTypes": {0: "HRP_IMAGE", 1: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "TreeGroup": "General"
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {
        "key":{"name": "Key",
                    "type": HARPIA_STRING,
                    "value": self.key
                    }
        }

# ------------------------------------------------------------------------------
