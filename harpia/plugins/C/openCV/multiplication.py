#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin

class Multiplication(OpenCVPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)

        self.help = "Realiza a multiplicação de duas imagens."

        self.description = {
            "Label": "Multiplication",
            "Icon": "images/multiplication.png",
            "Color": "180:10:10:150",
            "InTypes": {0: "HRP_IMAGE", 1: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "TreeGroup": "Arithmetic and logical operations"
        }

        self.properties = {}

        #-------------------C/OpenCv code------------------------------------
        self.vars = ""

        self.function_call = \
            '\nif(block$id$_img_i0 && block$id$_img_i1){\n' + \
            '\tblock$id$_img_o0 = cvCloneImage(block$id$_img_i0);\n' + \
            '\tadjust_images_size(block$id$_img_i0, block$id$_img_i1, block$id$_img_o0);\n' + \
            '\tcvMul(block$id$_img_i0, block$id$_img_i1, block$id$_img_o0,1);\n' + \
            '\tcvResetImageROI(block$id$_img_o0);\n' + \
            '}\n'

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
    def generate_header(self):
        return self.get_adjust_images_size()

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return self.function_call

# ------------------------------------------------------------------------------

