#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class NewInt(OpenCVPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.intVal = 1

        # Appearance
        self.help = "Creates new literal value (Int)."
        self.label = "New Int"
        self.icon = "images/newDouble.png"
        self.color = "50:50:200:150"
        self.out_types = ["HRP_INT"]
        self.group = "Basic Data Type"

        self.properties = {
            "intVal": {
                "name": "Value",
                "type": HARPIA_INT,
                "lower": 0,
                "upper": 65535,
                "step": 1
            }
        }

        # -------------------C/OpenCv code------------------------------------
        self.vars = 'int  block$id$_int_o0 = $intVal$; // New Int Out\n'

# ------------------------------------------------------------------------------
