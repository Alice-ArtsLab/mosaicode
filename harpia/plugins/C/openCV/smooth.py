#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class Smooth(OpenCVPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.smooth_type = "CV_GAUSSIAN"
        self.param1 = 7
        self.param2 = 9

        # Appearance
        self.help = "Aplicação de um filtro de suavização. " + \
            "Suaviza os contornos de objetos na imagem, borrando-os levemente."
        self.label = "Smooth"
        self.icon = "images/smooth.png"
        self.color = "50:125:50:150"
        self.in_types = ["HRP_IMAGE", "HRP_INT"]
        self.out_types = ["HRP_IMAGE", "HRP_INT", "HRP_INT"]
        self.group = "Filters and Color Conversion"

        self.properties = {
            "smooth_type": {
                "name": "Type",
                "type": HARPIA_COMBO,
                "values": ["CV_GAUSSIAN", "CV_BLUR", "CV_MEDIAN"]
            },
            "param1": {
                "name": "Parameter 1",
                "type": HARPIA_INT,
                "lower": 0,
                "upper": 99,
                "step": 1
            },
            "param2": {
                "name": "Parameter 2",
                "type": HARPIA_INT,
                "lower": 0,
                "upper": 99,
                "step": 1
            }
        }

        # -------------------C/OpenCv code------------------------------------
        self.vars = \
            'IplImage * block$id$_img_i0 = NULL;\n' + \
            'int block$id$_int_i1 = $param1$;\n' + \
            'int block$id$_int_i2 = $param2$;\n' + \
            'IplImage * block$id$_img_o0 = NULL;\n'

        self.function_call = \
            '\nif(block$id$_img_i0){\n' + \
            'block$id$_img_o0 = cvCloneImage(block$id$_img_i0);\n' + \
            'block$id$_int_i1 = (block$id$_int_i1 %2 == 0)? ' + \
            'block$id$_int_i1 + 1 : block$id$_int_i1;\n' + \
            'block$id$_int_i2 = (block$id$_int_i2 %2 == 0)? ' + \
            'block$id$_int_i2 + 1 : block$id$_int_i2;\n' + \
            'cvSmooth(block$id$_img_i0, block$id$_img_o0, ' + \
            '$smooth_type$,block$id$_int_i1,block$id$_int_i2,0,0);\n' + \
            '}\n'

# -----------------------------------------------------------------------------
