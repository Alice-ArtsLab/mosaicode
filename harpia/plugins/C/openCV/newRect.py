#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class NewRect(OpenCVPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.x0 = 0
        self.y0 = 0
        self.width = 640
        self.height = 480

        self.help = "Creates new rectangle"

        self.description = {
            'Label': 'New Rectangle',
            'Icon': 'images/newRect.png',
            'Color': '50:50:200:150',
            'InTypes': "",
            'OutTypes': {0: 'HRP_RECT'},
            'TreeGroup': 'Basic Data Type'
        }

        self.properties = {
            "x0": {
                "name": "X",
                "type": HARPIA_INT,
                "lower": 0,
                "upper": 65535,
                "step": 1
            },
            "y0": {
                "name": "Y",
                "type": HARPIA_INT,
                "lower": 0,
                "upper": 65535,
                "step": 1
            },
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
            'block$id$_rect_o0 = cvRect($x0$, $y0$, $width$, $height$);\n'

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
