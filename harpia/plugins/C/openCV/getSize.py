#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the GetSize class.
"""
from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class GetSize(OpenCVPlugin):
    """
    This class contains methods related the GetSize class.
    """
    # -------------------------------------------------------------------------

    def __init__(self):
        OpenCVPlugin.__init__(self)

        # Appearance
        self.help = "Extracts the input image size."
        self.label = "Get Size"
        self.color = "250:20:30:150"
        self.in_types = ["HRP_IMAGE"]
        self.out_types = ["HRP_RECT"]
        self.group = "Experimental"
        self.time_shifts = False

        # ------------------------------C/OpenCv code--------------------------
        self.function_call = \
            '\nif(block$id$_img_i0)\n{\n' + \
            '  \tblock$id$_rect_o0 = cvRect( 0, 0, ' + \
            'block$id$_img_i0->width, block$id$_img_i0->height);\n' + \
            '}\n'

# -----------------------------------------------------------------------------
