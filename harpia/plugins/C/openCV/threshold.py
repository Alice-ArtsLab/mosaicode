#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class Threshold(OpenCVPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.threshold = 122
        self.maxValue = 255
        self.thresholdType = "CV_THRESH_BINARY"

        self.help = "Operador de binarização da imagem, de acordo " + \
            "com um valor fixo de intensidade luminosa (valor de limiar)."

        self.description = {
            "Label": "Threshold",
            "Icon": "images/threshold.png",
            "Color": "50:125:50:150",
            "InTypes": {0: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "TreeGroup": "Filters and Color Conversion"
        }

        self.properties = {
            "threshold": {
                "name": "Threshold",
                "type": HARPIA_INT,
                "lower": 0,
                "upper": 255,
                "step": 1
            },
            "maxValue": {
                "name": "Max Gray Value",
                "type": HARPIA_INT,
                "lower": 0,
                "upper": 255,
                "step": 1
            },
            "thresholdType": {
                "name": "Threshold Type",
                "type": HARPIA_COMBO,
                "values": ["CV_THRESH_BINARY", "CV_THRESH_BINARY_INV",
                           "CV_THRESH_TRUNC", "CV_THRESH_TOZERO",
                           "CV_THRESH_TOZERO_INV"]
            }
        }

        # -------------------C/OpenCv code------------------------------------
        self.function_call = \
            '\nif(block$id$_img_i0){\n' + \
            'block$id$_img_o0 = cvCloneImage(block$id$_img_i0);\n' + \
            'cvThreshold(block$id$_img_i0, block$id$_img_o0, ' + \
            '$threshold$, $maxValue$, $thresholdType$);\n' + \
            '}\n'

    # ----------------------------------------------------------------------
    def get_help(self):
        return self.help

    # ----------------------------------------------------------------------
    def get_description(self):
        return self.description

    # ----------------------------------------------------------------------
    def get_properties(self):
        return self.properties

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return self.function_call

# -----------------------------------------------------------------------------
