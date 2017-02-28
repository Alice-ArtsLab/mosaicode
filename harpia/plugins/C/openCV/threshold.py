#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Threshold class.
"""
from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class Threshold(OpenCVPlugin):
    """
    This class contains methods related the Threshold class.
    """
    # -------------------------------------------------------------------------

    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.threshold = 122
        self.maxValue = 255
        self.thresholdType = "CV_THRESH_BINARY"

        # Appearance
        self.help = "Operador de binarização da imagem, de acordo " + \
            "com um valor fixo de intensidade luminosa (valor de limiar)."
        self.label = "Threshold"
        self.color = "50:125:50:150"
        self.in_types = ["HRP_IMAGE"]
        self.out_types = ["HRP_IMAGE"]
        self.group = "Filters and Color Conversion"

        self.properties = [{"name": "Threshold",
                            "label": "threshold",
                            "type": HARPIA_INT,
                            "lower": 0,
                            "upper": 255,
                            "step": 1
                            },
                           {"name": "Max Gray Value",
                            "label": "maxValue",
                            "type": HARPIA_INT,
                            "lower": 0,
                            "upper": 255,
                            "step": 1
                            },
                           {"name": "Threshold Type",
                            "label": "thresholdType",
                            "type": HARPIA_COMBO,
                            "values": ["CV_THRESH_BINARY",
                                       "CV_THRESH_BINARY_INV",
                                       "CV_THRESH_TRUNC",
                                       "CV_THRESH_TOZERO",
                                       "CV_THRESH_TOZERO_INV"]
                            }
                           ]

        # -------------------C/OpenCv code------------------------------------
        self.function_call = \
            '\nif(block$id$_img_i0){\n' + \
            'block$id$_img_o0 = cvCloneImage(block$id$_img_i0);\n' + \
            'cvThreshold(block$id$_img_i0, block$id$_img_o0, ' + \
            '$threshold$, $maxValue$, $thresholdType$);\n' + \
            '}\n'

# -----------------------------------------------------------------------------
