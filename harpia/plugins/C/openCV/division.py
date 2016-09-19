#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin

class Division(OpenCVPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.id = -1
        self.type = self.__class__.__module__

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return"realiza a divisão de duas imagens."

    # ----------------------------------------------------------------------
    def generate_header(self):
        return self.get_adjust_images_size()

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return \
            'if(block$id$_img_i1 && block$id$_img_i2){\n' + \
            'block$id$_img_o1 = cvCloneImage(block$id$_img_i1);\n' + \
            'adjust_images_size(block$id$_img_i1, block$id$_img_i2, block$id$_img_o1);\n' + \
            'cvDiv(block$id$_img_i1, block$id$_img_i2, block$id$_img_o1,1);\n' + \
            'cvResetImageROI(block$id$_img_o1);\n}\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            "Label": "Division",
            "Icon": "images/division.png",
            "Color": "180:10:10:150",
            "InTypes": {0: "HRP_IMAGE", 1: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "Description": "Divide two images.",
            "TreeGroup": "Arithmetic and logical operations"
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {}

# ------------------------------------------------------------------------------
