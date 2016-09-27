#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin

class Laplace(OpenCVPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.masksize = "3"

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "operação de filtragem que calcula o Laplaciano de uma imagem,\
        realçando cantos e bordas de objetos."

    # ----------------------------------------------------------------------
    def generate_vars(self):
        self.masksize = int(self.masksize)
        return \
            'IplImage * block$id$_img_i0 = NULL; //Laplace In \n' + \
            'IplImage * block$id$_img_o0 = NULL; //Laplace Out \n' + \
            'int block$id$_int_i1 = $masksize$; // Laplace Mask Size\n'

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return \
            '\nif(block$id$_img_i0){\n' + \
            'block$id$_int_i1 = (block$id$_int_i1 > 31)? 31 : block$id$_int_i1; // Laplace Mask Constraint\n' + \
            'block$id$_int_i1 = (block$id$_int_i1 % 2 == 0)? block$id$_int_i1 + 1 : block$id$_int_i1; // Only Odd\n' + \
            'CvSize size$id$ = cvGetSize(block$id$_img_i0);\n'+ \
            'block$id$_img_o0 = cvCreateImage(size$id$, IPL_DEPTH_32F,block$id$_img_i0->nChannels);\n' + \
            'cvLaplace(block$id$_img_i0, block$id$_img_o0 , block$id$_int_i1);}\n'

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Label": "Laplace",
            "Icon": "images/laplace.png",
            "Color": "250:180:80:150",
            "InTypes": {0: "HRP_IMAGE", 1: "HRP_INT"},
            "OutTypes": {0: "HRP_IMAGE"},
            "TreeGroup": "Gradients, Edges and Corners"
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {
        "masksize":{"name": "Mask Size",
                    "type": HARPIA_COMBO,
                    "value": self.masksize,
                    "values": ["1", "3", "5", "7", "9", "11", "13"]
                    }
        }

# ------------------------------------------------------------------------------

