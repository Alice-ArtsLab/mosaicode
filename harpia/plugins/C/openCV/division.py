#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Division class.
"""
from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class Division(OpenCVPlugin):
    """
    This class contains methods related the Division class.
    """

    # -------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)

        # Appearance
        self.help = "Realiza a divisão de duas imagens."
        self.label = "Division"
        self.icon = "images/division.png"
        self.color = "180:10:10:150"
        self.in_types = ["HRP_IMAGE", "HRP_IMAGE"]
        self.out_types = ["HRP_IMAGE"]
        self.group = "Arithmetic and logical operations"

        # -----------------------------C/OpenCv code---------------------------
        self.header = self.get_adjust_images_size()

        self.function_call = \
            'if(block$id$_img_i0 && block$id$_img_i1){\n' + \
            'block$id$_img_o0 = cvCloneImage(block$id$_img_i0);\n' + \
            'adjust_images_size(block$id$_img_i0, ' + \
            'block$id$_img_i1, block$id$_img_o0);\n' + \
            'cvDiv(block$id$_img_i0, block$id$_img_i1, ' + \
            'block$id$_img_o0,1);\n' + \
            'cvResetImageROI(block$id$_img_o0);\n}\n'

# -----------------------------------------------------------------------------
