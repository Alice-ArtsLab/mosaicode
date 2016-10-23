#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class Select(OpenCVPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.key = "a"

        # Appearance
        self.help = "Select between two images."
        self.label = "Select"
        self.icon = "images/select.png"
        self.color = "50:100:200:150"
        self.in_types = ["HRP_IMAGE", "HRP_IMAGE"]
        self.out_types = ["HRP_IMAGE"]
        self.group = "General"

        self.properties = {
            "key": {
                "name": "Key",
                "type": HARPIA_STRING,
                "maxlength": 1
            }
        }

        # -------------------C/OpenCv code------------------------------------
        self.vars = 'char block$id$_key = \'$key$\';\n'

        self.function_call = 'if(block$id$_img_i0 && block$id$_img_i1){\n' + \
            'if (key != -1)\n' + \
            '\tblock$id$_key = key;\n' + \
            'if (block$id$_key == \'$key$\' )\n' + \
            '\tblock$id$_img_o0 = cvCloneImage(block$id$_img_i0);\n' + \
            'else\n' + \
            '\tblock$id$_img_o0 = cvCloneImage(block$id$_img_i1);\n' + \
            '}\n'

# -----------------------------------------------------------------------------
