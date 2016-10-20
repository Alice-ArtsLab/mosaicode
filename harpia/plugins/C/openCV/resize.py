#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class Resize(OpenCVPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.method = "CV_INTER_LINEAR"

        self.help = "Resizes the input image to the " + \
            "dimensions of the input rectangle."

        self.description = {
            "Label": "Resize Image",
            "Icon": "images/resize.png",
            "Color": "20:80:10:150",
            "InTypes": {0: "HRP_IMAGE", 1: "HRP_RECT"},
            "OutTypes": {0: "HRP_IMAGE"},
            "TreeGroup": "Experimental"
        }

        self.properties = {
            "method": {
                "name": "Method",
                "type": HARPIA_COMBO,
                "values": ["CV_INTER_NN", "CV_INTER_LINEAR",
                           "CV_INTER_AREA", "CV_INTER_CUBIC"]
            }
        }

        # -------------------C/OpenCv code------------------------------------
        self.function_call = \
            'if(block$id$_img_i0){\n' + \
            'CvSize size$id$ = cvSize(block$id$_rect_i1.width,' + \
            'block$id$_rect_i1.height);\n' + \
            'block$id$_img_o0 = cvCreateImage(size$id$, ' + \
            'block$id$_img_i0->depth,block$id$_img_i0->nChannels);\n' + \
            'cvResize(block$id$_img_i0, block$id$_img_o0, $method$);\n' + \
            '}\n'

# -----------------------------------------------------------------------------
