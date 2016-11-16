#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class Pow(OpenCVPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.exponent = 1

        # Appearance
        self.help = "Eleva cada ponto de uma " + \
            "imagem a um valor fixo de potência."
        self.label = "Pow"
        self.icon = "images/pow.png"
        self.color = "230:230:60:150"
        self.in_types = ["HRP_IMAGE"]
        self.out_types = ["HRP_IMAGE"]
        self.group = "Math Functions"

        self.properties = [{"name": "Exponent",
                            "label": "exponent",
                            "type": HARPIA_INT,
                            "lower": 1,
                            "upper": 10,
                            "step": 1
                            }
                           ]

        # -------------------C/OpenCv code------------------------------------
        self.function_call = \
            '\nif(block$id$_img_i0){\n' + \
            'block$id$_img_o0 = cvCloneImage(block$id$_img_i0);\n' + \
            'cvPow(block$id$_img_i0, block$id$_img_o0, $exponent$);\n' + \
            '}\n'

# -----------------------------------------------------------------------------
