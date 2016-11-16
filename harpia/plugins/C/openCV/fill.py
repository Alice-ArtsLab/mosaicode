#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class Fill(OpenCVPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.rect_color = "#0000ffff0000"

        # Appearance
        self.help = "Preenche toda a imagem de uma cor."
        self.label = "Fill image"
        self.icon = "images/fill.png"
        self.color = "50:100:200:150"
        self.in_types = ["HRP_IMAGE"]
        self.out_types = ["HRP_IMAGE"]
        self.group = "General"

        self.properties = [{"name": "rect_Color",
                            "label": "rect_color",
                            "type": HARPIA_COLOR
                            }
                           ]

        # ------------------------------C/OpenCv code--------------------------

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        # --------define RGB-------------
        red = self.rect_color[1:5]
        green = self.rect_color[5:9]
        blue = self.rect_color[9:13]

        red = int(red, 16) / 257
        green = int(green, 16) / 257
        blue = int(blue, 16) / 257

        return \
            'if(block$id$_img_i0){\n' + \
            '\tblock$id$_img_o0 = cvCloneImage(block$id$_img_i0);\n' + \
            '\tCvScalar color = cvScalar' + \
            '(' + str(blue) + ',' + str(green) + ',' + str(red) + ',0);\n' + \
            '\tcvSet(block$id$_img_o0, color, NULL);\n' + \
            '}\n'

# -----------------------------------------------------------------------------
