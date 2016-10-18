#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class NewPoint(OpenCVPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.x0 = 0
        self.y0 = 0

        self.help = "Creates a new Point."

        self.description = {
            'Label': 'New Point',
            'Icon': 'images/newPoint.png',
            'Color': '50:50:200:150',
            'InTypes': "",
            'OutTypes': {0: 'HRP_POINT'},
            'TreeGroup': 'Basic Data Type'
        }

        self.properties = {
            "x0": {
                "name": "X",
                "type": HARPIA_INT,
                "lower": 0,
                "upper": 65535,
                "step": 1
            },
            "y0": {
                "name": "Y",
                "type": HARPIA_INT,
                "lower": 0,
                "upper": 65535,
                "step": 1
            }
        }

        # -------------------C/OpenCv code------------------------------------
        self.vars = 'CvPoint block$id$_point_o0 = cvPoint($x0$,$y0$);\n'

        self.function_call = \
            'block$id$_point_o0 = cvPoint($x0$,$y0$);\n'

# ------------------------------------------------------------------------------
