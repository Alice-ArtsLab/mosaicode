#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the NewRect class.
"""
from harpia.GUI.fieldtypes import *
from harpia.plugins.c.opencv.opencvplugin import OpenCVPlugin


class NewRect(OpenCVPlugin):
    """
    This class contains methods related the NewRect class.
    """
    # -------------------------------------------------------------------------

    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.help = "Creates new rectangle"
        self.label = "New Rectangle"
        self.color = "50:50:200:150"
        self.out_ports = [{"type":"HRP_RECT",
                          "name":"size",
                          "label":"Size"}]
        self.group = "Basic Data Type"

        self.properties = [{"label": "X",
                            "name": "x0",
                            "type": HARPIA_INT,
                            "lower": 0,
                            "upper": 65535,
                            "step": 1,
                            "value":0
                            },
                           {"label": "Y",
                            "name": "y0",
                            "type": HARPIA_INT,
                            "lower": 0,
                            "upper": 65535,
                            "step": 1,
                            "value":0
                            },
                           {"label": "Width",
                            "name": "width",
                            "type": HARPIA_INT,
                            "lower": 0,
                            "upper": 65535,
                            "step": 1,
                            "value":640
                            },
                           {"label": "Height",
                            "name": "height",
                            "type": HARPIA_INT,
                            "lower": 0,
                            "upper": 65535,
                            "step": 1,
                            "value":480
                            }
                           ]

        # -------------------C/OpenCv code------------------------------------
        self.function_call = \
            'block$id$_rect_o0 = cvRect($x0$, $y0$, $width$, $height$);\n'

# -----------------------------------------------------------------------------
