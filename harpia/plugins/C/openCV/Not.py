#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin

class Not(OpenCVPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Realiza a negação lógica de uma imagem. Corresponde à negativa da imagem."

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return \
            'if(block$id$_img_i0){\n' + \
            'block$id$_img_o0 = cvCloneImage(block$id$_img_i0);\n' + \
            'cvNot(block$id$_img_i0, block$id$_img_o0);\n' + \
            '}\n'

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Label": "Not",
            "Icon": "images/not.png",
            "Color": "10:180:10:150",
            "InTypes": {0: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "TreeGroup": "Arithmetic and logical operations"
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {}

# ------------------------------------------------------------------------------
