#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the NewInt class.
"""
from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class NewInt(OpenCVPlugin):
    """
    This class contains methods related the NewInt class.
    """
    # -------------------------------------------------------------------------

    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.intVal = 1

        # Appearance
        self.help = "Creates new literal value (Int)."
        self.label = "New Int"
        self.color = "50:50:200:150"
        self.out_types = ["HRP_INT"]
        self.group = "Basic Data Type"

        self.properties = [{"name": "Value",
                            "label": "intVal",
                            "type": HARPIA_INT,
                            "lower": 0,
                            "upper": 65535,
                            "step": 1
                            }
                           ]

        # -------------------C/OpenCv code------------------------------------
        self.vars = 'int  block$id$_int_o0 = $intVal$; // New Int Out\n'

# ------------------------------------------------------------------------------
