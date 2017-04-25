#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Slider class.
"""
from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin


class Slider(Plugin):
    """
    This class contains methods related the Slider class.
    """
    # -------------------------------------------------------------------------

    def __init__(self):
        Plugin.__init__(self)
        self.help = "Creates Slider to int value."
        self.label = "Slider"
        self.color = "50:50:200:150"
        self.out_ports = [{"type":"harpia.extensions.c.ports.int",
                          "name":"slider_value",
                          "label":"Slider Value"}]
        self.group = "Basic Data Type"

        self.properties = [{"label": "Value",
                            "name": "intVal",
                            "type": HARPIA_INT,
                            "lower": 0,
                            "upper": 65535,
                            "step": 1,
                            "value":1
                            },
                           {"label": "Max Value",
                            "name": "maxVal",
                            "type": HARPIA_INT,
                            "lower": 0,
                            "upper": 65535,
                            "step": 1,
                            "value":31
                            },
                           {"label": "Label",
                            "name": "label",
                            "type": HARPIA_STRING,
                            "value":"label"
                            },
                           {"label": "Window Title",
                            "name": "window_name",
                            "type": HARPIA_STRING,
                            "value":"My Image"
                            }
                           ]

        # -------------------C/OpenCv code------------------------------------
        self.codes[1] = \
            'int  block$id$_int_o0 = $intVal$; // New Int Out\n'

        self.codes[2] = \
            'cvNamedWindow("$window_name$",CV_WINDOW_AUTOSIZE );\n' + \
            'cvCreateTrackbar("$label$", "$window_name$",' + \
            ' &block$id$_int_o0, $maxVal$, NULL);\n'


        self.language = "c"
        self.framework = "opencv"
# -----------------------------------------------------------------------------
