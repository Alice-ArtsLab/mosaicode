#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class NewImage(OpenCVPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.width = "640"
        self.height = "480"

        # Appearance
        self.help = "Cria uma nova imagem."
        self.label = "New Image"
        self.icon = "images/acquisition.png"
        self.color = "50:100:200:150"
        self.out_types = ["HRP_IMAGE"]
        self.group = "Image Source"

        self.properties = {
            "width": {
                "name": "Width",
                "type": HARPIA_INT,
                "lower": 0,
                "upper": 65535,
                "step": 1
            },
            "height": {
                "name": "Height",
                "type": HARPIA_INT,
                "lower": 0,
                "upper": 65535,
                "step": 1
            }
        }

        # -------------------C/OpenCv code------------------------------------
        self.function_call = \
            'CvSize size$id$ = cvSize($width$,$height$);\n' + \
            'block$id$_img_o0 = cvCreateImage(size$id$,IPL_DEPTH_8U,3);\n' + \
            'cvSetZero(block$id$_img_o0);\n'

# ------------------------------------------------------------------------------
