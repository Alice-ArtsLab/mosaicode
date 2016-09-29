#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin

class Erode(OpenCVPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.masksize = "3x3"
        self.iterations = 1

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "operação morfológica que provoca erosão nos objetos de uma imagem, reduzindo suas dimensões."

    # ----------------------------------------------------------------------
    def generate_vars(self):
        self.iterations = int(float(self.iterations))
        return \
            'IplImage * block$id$_img_i0 = NULL; // ERODE input\n' + \
            'int block$id$_int_i1 = $iterations$; // ERODE iterarions\n' + \
            'IplImage * block$id$_img_o0 = NULL; // ERODE output\n' + \
            'IplConvKernel * block$id$_arg_mask = cvCreateStructuringElementEx(' + self.masksize[0] + \
                    ' , ' + self.masksize[2] + ', 1, 1,CV_SHAPE_RECT,NULL);\n'

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return \
            '\nif(block$id$_img_i0){\n' + \
            'block$id$_img_o0 = cvCloneImage(block$id$_img_i0);\n' + \
            'cvErode(block$id$_img_i0, block$id$_img_o0, block$id$_arg_mask, block$id$_int_i1);\n'+ \
            '}\n'

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Label": "Erosion",
            "Icon": "images/erode.png",
            "Color": "180:230:220:150",
            "InTypes": {0: "HRP_IMAGE", 1: "HRP_INT"},
            "OutTypes": {0: "HRP_IMAGE"},
            "TreeGroup": "Morphological Operations"
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {
        "masksize":{"name": "Mask Size",
                    "type": HARPIA_COMBO,
                    "value": self.masksize,
                    "values": ["1x1", "3x3", "5x5", "7x7"]
                    },
        "iterations":{"name": "Iterations",
                    "type": HARPIA_INT,
                    "value": self.iterations,
                    "lower":0,
                    "upper":65535,
                    "step":1
                    }
        }

# ------------------------------------------------------------------------------
