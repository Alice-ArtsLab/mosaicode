#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class Slider(OpenCVPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.intVal = 1
        self.maxVal = 31
        self.label = "Value"
        self.window_name = "My Image"

        self.help = "Creates Slider to int value."

        self.description = {
            'Label': 'Slider',
            'Icon': 'images/newDouble.png',
            'Color': '50:50:200:150',
            'InTypes': "",
            'OutTypes': {0: 'HRP_INT'},
            'TreeGroup': 'Basic Data Type'
        }

        self.properties = {
            "intVal": {
                "name": "Value",
                "type": HARPIA_INT,
                "lower": 0,
                "upper": 65535,
                "step": 1
            },
            "maxVal": {
                "name": "Max Value",
                "type": HARPIA_INT,
                "lower": 0,
                "upper": 65535,
                "step": 1
            },
            "label": {
                "name": "Label",
                "type": HARPIA_STRING
            },
            "window_name": {
                "name": "Window Title",
                "type": HARPIA_STRING
            }
        }

        # -------------------C/OpenCv code------------------------------------
        self.vars = \
            'int  block$id$_int_o0 = $intVal$; // New Int Out\n'

        self.function_call = \
            'cvNamedWindow("$window_name$",CV_WINDOW_AUTOSIZE );\n' + \
            'cvCreateTrackbar("$label$", "$window_name$",' + \
            ' &block$id$_int_o0, $maxVal$, NULL);\n'

# -----------------------------------------------------------------------------
