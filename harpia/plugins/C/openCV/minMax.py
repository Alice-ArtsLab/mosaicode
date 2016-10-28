#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class MinMax(OpenCVPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.minX = 0
        self.maxX = 500
        self.minY = 0
        self.maxY = 500
        self.minVal = 0
        self.maxVal = 500
        self.minORmax = "min"
        self.criteria = "pos"

        # Appearance
        self.help = "Finds min or max from input image and judges " + \
            "it according to a custom criteria."
        self.label = "Find Min or Max"
        self.icon = "images/minMax.png"
        self.color = "50:50:200:150"
        self.in_types = ["HRP_IMAGE"]
        self.out_types = ["HRP_DOUBLE", "HRP_POINT"]
        self.group = "Feature Detection"

        self.properties = {
            "minX": {
                "name": "Min X",
                "type": HARPIA_INT,
                "lower": 0,
                "upper": 65535,
                "step": 1
            },
            "maxX": {
                "name": "Max X",
                "type": HARPIA_INT,
                "lower": 0,
                "upper": 65535,
                "step": 1
            },
            "minY": {
                "name": "Min Y",
                "type": HARPIA_INT,
                "lower": 0,
                "upper": 65535,
                "step": 1
            },
            "maxY": {
                "name": "Max Y",
                "type": HARPIA_INT,
                "lower": 0,
                "upper": 65535,
                "step": 1
            },
            "minVal": {
                "name": "Min Val",
                "type": HARPIA_INT,
                "lower": 0,
                "upper": 65535,
                "step": 1
            },
            "maxVal": {
                "name": "Max Val",
                "type": HARPIA_INT,
                "lower": 0,
                "upper": 65535,
                "step": 1
            },
            "minORmax": {
                "name": "Min Or Max",
                "type": HARPIA_COMBO,
                "values": ["min", "max"]
            },
            "criteria": {
                "name": "Criteria",
                "type": HARPIA_COMBO,
                "values": ["pos", "val"]
            }
        }
        # ------------------------------C/OpenCv code--------------------------

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        value = '\nif(block$id$_img_i0)\n{\n' + \
                '   double minVal,maxVal;\n' + \
                '   CvPoint minP,maxP;\n' + \
                '   block$id$_double_o0 = 0;\n' + \
                '   cvMinMaxLoc(block$id$_img_i0, &minVal, ' + \
                '&maxVal, &minP, &maxP, NULL);\n'
        if self.minORmax == 'max':
            value += '  minP = maxP;\n' + \
                '   minVal = maxVal;\n'

        value += '  block$id$_point_o1 = minP;\n'

        if self.criteria == "pos":
            value += '  if(minP.x >= $minX$ && minP.x <= $maxX$)\n' + \
                '        if(minP.y >= $minY$ && minP.y <= $maxY$)\n' + \
                '           block$id$_double_o0 = 1.0;\n'
        elif self.criteria == "val":
            value += '  if(minVal >= $minVal$ && minVal <= $maxVal$)\n' + \
                '        block$id$_double_o0 = 1.0;\n'
        value += '}\n'

        return value

# -----------------------------------------------------------------------------
