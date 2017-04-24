#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the NewPoint class.
"""
from harpia.GUI.fieldtypes import *
from harpia.extensions.c.opencv.opencvplugin import OpenCVPlugin


class NewPoint(OpenCVPlugin):
    """
    This class contains methods related the NewPoint class.
    """

    # -------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.x0 = 0
        self.y0 = 0

        # Appearance
        self.help = "Creates a new Point."
        self.label = "New Point"
        self.color = "50:50:200:150"
        self.out_types = ["harpia.extensions.c.ports.point"]
        self.group = "Basic Data Type"

        self.properties = [{"name": "X",
                            "label": "x0",
                            "type": HARPIA_INT,
                            "lower": 0,
                            "upper": 65535,
                            "step": 1
                            },
                           {"name": "Y",
                            "label": "y0",
                            "type": HARPIA_INT,
                            "lower": 0,
                            "upper": 65535,
                            "step": 1
                            }
                           ]

        # -------------------C/OpenCv code------------------------------------
        self.codes[1] = 'CvPoint block$id$_point_o0 = cvPoint($x0$,$y0$);\n'

        self.codes[2] = \
            'block$id$_point_o0 = cvPoint($x0$,$y0$);\n'

# ------------------------------------------------------------------------------
