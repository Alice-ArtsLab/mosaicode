#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class NewDouble(OpenCVPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.doubleVal = 1

        self.help = "Creates new literal value (Double)."

        self.description = {
            'Label': 'New Double',
            'Icon': 'images/newDouble.png',
            'Color': '50:50:200:150',
            'InTypes': "",
            'OutTypes': {0: 'HRP_DOUBLE'},
            'TreeGroup': 'Basic Data Type'
        }

        self.properties = {
            "doubleVal": {
                "name": "Value",
                "type": HARPIA_FLOAT,
                "lower": 0,
                "upper": 65535,
                "step": 1
            }
        }

        # -------------------C/OpenCv code------------------------------------
        self.vars = 'double block$id$_double_o0 = ' + \
            '$doubleVal$; // New Double Out\n'

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
    def generate_vars(self):
        return self.vars

# -----------------------------------------------------------------------------
