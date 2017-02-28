#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the AddBorder class.
"""
from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class AddBorder(OpenCVPlugin):
    """
    This class contains methods related the AddBorder class.
    """
    # -------------------------------------------------------------------------

    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.border = 50
        self.color = "#0000ffff0000"
        self.border_type = "IPL_BORDER_CONSTANT"

        self.red = self.color[1:5]
        self.green = self.color[5:9]
        self.blue = self.color[9:13]

        self.red = int(self.red, 16) / 257
        self.green = int(self.green, 16) / 257
        self.blue = int(self.blue, 16) / 257

        # Appearance
        self.help = "Adiciona bordas na imagem."
        self.label = "Add Border"
        self.color = "0:180:210:150"
        self.in_types = ["HRP_IMAGE", "HRP_INT"]
        self.out_types = ["HRP_IMAGE"]
        self.group = "Experimental"

        self.properties = [{"name": "Color",
                            "label": "color",
                            "type": HARPIA_COLOR
                            },
                           {"name": "Type",
                            "label": "border_type",
                            "type": HARPIA_COMBO,
                            "values": ["IPL_BORDER_CONSTANT",
                                       "IPL_BORDER_REPLICATE",
                                       "IPL_BORDER_REFLECT",
                                       "IPL_BORDER_WRAP"]
                            },
                           {"name": "Border Size",
                            "label": "border",
                            "type": HARPIA_INT
                            }
                           ]

        # --------------------c/OpneCV code----------------------------
        self.vars = \
            "IplImage * block$id$_img_i0 = NULL;\n" + \
            "int block$id$_int_i1 = $border$;\n" + \
            "IplImage * block$id$_img_o0 = NULL;\n"

        self.function_call = \
            'if(block$id$_img_i0){\n' + \
            '\tCvSize size$id$ = cvSize(block$id$_img_i0->width +' + \
            ' block$id$_int_i1 * 2, block$id$_img_i0->height' + \
            ' + block$id$_int_i1 * 2);\n' + \
            '\tblock$id$_img_o0 = cvCreateImage(size$id$,' + \
            ' block$id$_img_i0->depth,block$id$_img_i0->nChannels);\n' + \
            '\tCvPoint point$id$ = cvPoint' + \
            '(block$id$_int_i1, block$id$_int_i1);\n' + \
            '\tCvScalar color = cvScalar($blue$,$green$,$red$,0);\n' + \
            '\tcvCopyMakeBorder(block$id$_img_i0, block$id$_img_o0,' + \
            ' point$id$, $border_type$, color);\n' + \
            '}\n'

    # ----------------------------------------------------------------------
    def set_properties(self, data):
        OpenCVPlugin.set_properties(self, data)
        self.red = self.color[1:5]
        self.green = self.color[5:9]
        self.blue = self.color[9:13]

        self.red = int(self.red, 16) / 257
        self.green = int(self.green, 16) / 257
        self.blue = int(self.blue, 16) / 257

# -----------------------------------------------------------------------------
