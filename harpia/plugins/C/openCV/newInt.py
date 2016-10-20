#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class NewInt(OpenCVPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.intVal = 1

        self.help = "Creates new literal value (Int)."

        self.description = {
            'Label': 'New Int',
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
            }
        }

        # -------------------C/OpenCv code------------------------------------
        self.vars = 'int  block$id$_int_o0 = $intVal$; // New Int Out\n'

# ------------------------------------------------------------------------------
