#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class FillRect(OpenCVPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.rect_color = "#0000ffff0000"

        # Appearance
        self.help = "Preenche o retângulo de uma cor."
        self.label = "Fill Rectangle"
        self.icon = "images/fill.png"
        self.color = "50:100:200:150"
        self.in_types = ["HRP_IMAGE", "HRP_RECT"]
        self.out_types = ["HRP_IMAGE"]
        self.group = "Basic Shapes"

        self.properties = [{"name": "rect_Color",
                            "label": "rect_color",
                            "type": HARPIA_COLOR
                            }
                           ]

        # ------------------------------C/OpenCv code--------------------------
        self.vars = \
            'IplImage * block$id$_img_i0 = NULL;\n' + \
            'CvRect block$id$_rect_i1;\n' + \
            'IplImage * block$id$_img_o0 = NULL;\n'

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        red = self.rect_color[1:5]
        green = self.rect_color[5:9]
        blue = self.rect_color[9:13]

        red = int(red, 16) / 257
        green = int(green, 16) / 257
        blue = int(blue, 16) / 257
        return \
            '\nif(block$id$_img_i0)\n{\n' + \
            '\tblock$id$_img_o0 = cvCloneImage(block$id$_img_i0);\n' + \
            '\tcvSetImageROI(block$id$_img_o0 , block$id$_rect_i1);\n' + \
            '\tCvScalar color = cvScalar(' + str(blue) + ',' + str(green) + \
            ',' + str(red) + ',0);\n' + \
            '\tcvSet(block$id$_img_o0,color,NULL);\n' + \
            '\tcvResetImageROI(block$id$_img_o0);\n' + \
            '}\n'

# -----------------------------------------------------------------------------
