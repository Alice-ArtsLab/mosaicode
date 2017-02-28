#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Slider class.
"""
from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class Slider(OpenCVPlugin):
    """
    This class contains methods related the Slider class.
    """
    # -------------------------------------------------------------------------

    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.intVal = 1
        self.maxVal = 31
        self.label = "Value"
        self.window_name = "My Image"

        # Appearance
        self.help = "Creates Slider to int value."
        self.label = "Slider"
        self.color = "50:50:200:150"
        self.out_types = ["HRP_INT"]
        self.group = "Basic Data Type"

        self.properties = [{"name": "Value",
                            "label": "intVal",
                            "type": HARPIA_INT,
                            "lower": 0,
                            "upper": 65535,
                            "step": 1
                            },
                           {"name": "Max Value",
                            "label": "maxVal",
                            "type": HARPIA_INT,
                            "lower": 0,
                            "upper": 65535,
                            "step": 1
                            },
                           {"name": "Label",
                            "label": "label",
                            "type": HARPIA_STRING
                            },
                           {"name": "Window Title",
                            "label": "window_name",
                            "type": HARPIA_STRING
                            }
                           ]

        # -------------------C/OpenCv code------------------------------------
        self.vars = \
            'int  block$id$_int_o0 = $intVal$; // New Int Out\n'

        self.function_call = \
            'cvNamedWindow("$window_name$",CV_WINDOW_AUTOSIZE );\n' + \
            'cvCreateTrackbar("$label$", "$window_name$",' + \
            ' &block$id$_int_o0, $maxVal$, NULL);\n'

# -----------------------------------------------------------------------------
