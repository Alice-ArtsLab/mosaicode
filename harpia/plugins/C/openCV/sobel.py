#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin

class Sobel(OpenCVPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.masksize = 3
        self.xorder = 1
        self.yorder = 1

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Operação de filtragem que utiliza uma máscara Sobel para realçar cantos e bordas da imagem."

    # ----------------------------------------------------------------------
    def generate_vars(self):
        return \
            'IplImage * block$id$_img_i0 = NULL;\n' + \
            'IplImage * block$id$_img_o0 = NULL;\n' + \
            'IplImage * block$id$_img_t = NULL;\n'

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return \
            '\nif(block$id$_img_i0){\n' + \
            'CvSize size$id$ = cvGetSize(block$id$_img_i0);\n'+ \
            'block$id$_img_o0 = cvCreateImage(size$id$, IPL_DEPTH_32F,block$id$_img_i0->nChannels);\n' + \
            'cvSobel(block$id$_img_i0, block$id$_img_o0 ,$xorder$, $yorder$, $masksize$);\n'+ \
            '}\n'

    # ----------------------------------------------------------------------
    def generate_dealloc(self):
        return 'cvReleaseImage(&block$id$_img_o0);\n' + \
               'cvReleaseImage(&block$id$_img_i0);\n' + \
               'cvReleaseImage(&block$id$_img_t);\n'

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Label": "Sobel",
            "Icon": "images/sobel.png",
            "Color": "250:180:80:150",
            "InTypes": {0: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "TreeGroup": "Gradients, Edges and Corners"
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {"xorder":{"name": "X Axis Derivate Order",
                            "type": HARPIA_INT,
                            "value": self.xorder,
                            "lower":0,
                            "upper":6,
                            "step":1
                            },
                "yorder":{"name": "Y Axis Derivate Order",
                            "type": HARPIA_INT,
                            "value": self.yorder,
                            "lower":0,
                            "upper":6,
                            "step":1
                            },
                "masksize":{"name": "Mask Size",
                            "type": HARPIA_INT,
                            "value": self.masksize,
                            "lower":1,
                            "upper":7,
                            "step":2
                            }
                 }

# ------------------------------------------------------------------------------
