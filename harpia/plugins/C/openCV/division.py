#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class Division(OpenCVPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)

        self.help = "Realiza a divisão de duas imagens."

        self.description = {
            "Label": "Division",
            "Icon": "images/division.png",
            "Color": "180:10:10:150",
            "InTypes": {0: "HRP_IMAGE", 1: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "TreeGroup": "Arithmetic and logical operations"
        }

        # -----------------------------C/OpenCv code---------------------------
        self.vars = ""

        self.function_call = \
            'if(block$id$_img_i0 && block$id$_img_i1){\n' + \
            'block$id$_img_o0 = cvCloneImage(block$id$_img_i0);\n' + \
            'adjust_images_size(block$id$_img_i0, ' + \
            'block$id$_img_i1, block$id$_img_o0);\n' + \
            'cvDiv(block$id$_img_i0, block$id$_img_i1, ' + \
            'block$id$_img_o0,1);\n' + \
            'cvResetImageROI(block$id$_img_o0);\n}\n'

# -----------------------------------------------------------------------------
