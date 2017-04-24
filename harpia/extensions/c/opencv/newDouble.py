#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the NewDouble class.
"""
from harpia.GUI.fieldtypes import *
from harpia.extensions.c.opencv.opencvplugin import OpenCVPlugin


class NewDouble(OpenCVPlugin):
    """
    This class contains methods related the NewDouble class.
    """
    # -------------------------------------------------------------------------

    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.doubleVal = 1

        # Appearance
        self.help = "Creates new literal value (Double)."
        self.label = "New Double"
        self.color = "50:50:200:150"
        self.out_types = ["harpia.extensions.c.ports.double"]
        self.group = "Basic Data Type"

        self.properties = [{"name": "Value",
                            "label": "doubleVal",
                            "type": HARPIA_FLOAT,
                            "lower": 0,
                            "upper": 65535,
                            "step": 1
                            }
                           ]

        # -------------------C/OpenCv code------------------------------------
        self.codes[1] = 'double block$id$_double_o0 = ' + \
            '$doubleVal$; // New Double Out\n'

# -----------------------------------------------------------------------------
