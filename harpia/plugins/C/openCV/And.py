#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin

class And(OpenCVPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.help = "Permite a operação lógica 'E' entre as duas entradas. Para esse bloco há duas possibilidades." + \
        "Primeira: Executa a operação entre duas imagens ponto a ponto." + \
        "Segunda: Executa a operação entre um valor constante e cada ponto da imagem."

        self.description = { 
            "Label": "And",
            "Icon": "images/and.png",
            "Color": "10:180:10:150",
            "InTypes": {0: "HRP_IMAGE", 1: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "TreeGroup": "Arithmetic and logical operations"
        }

        #--------------------c/OpneCV code----------------------------
        self.function_call = \
            '\nif(block$id$_img_i0 && block$id$_img_i1){\n' + \
            '\tblock$id$_img_o0 = cvCloneImage(block$id$_img_i0);\n' + \
            '\tadjust_images_size(block$id$_img_i0, block$id$_img_i1, block$id$_img_o0);\n' + \
            '\tcvAnd(block$id$_img_i0, block$id$_img_i1, block$id$_img_o0,0);\n' + \
            '\tcvResetImageROI(block$id$_img_o0);\n' + \
            '}\n'
            
    # ----------------------------------------------------------------------
    def get_help(self):
        return self.help

    # ------------------------------------------------------------------------------
    def get_description(self):
        return self.description

    # ------------------------------------------------------------------------------
    def get_properties(self):
        return {}

    # ----------------------------------------------------------------------
    def generate_header(self):
        return self.get_adjust_images_size()

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return self.function_call

# ------------------------------------------------------------------------------
