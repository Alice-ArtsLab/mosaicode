#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Closing class.
"""
from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class Closing(OpenCVPlugin):
    """
    This class contains methods related the Closing class.
    """

    # -------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.masksize = "7x7"

        # Appearance
        self.help = "Operação de morfologia matemática para realizar o " + \
            "fechamento da imagem de acordo com o elemento estruturante." + \
            "Equivale a aplicação de uma dilatação seguida de uma erosão."
        self.label = "Closing"
        self.icon = "images/closing.png"
        self.color = "180:230:220:150"
        self.in_types = ["HRP_IMAGE", "HRP_INT", "HRP_INT"]
        self.out_types = ["HRP_IMAGE"]
        self.group = "Morphological Operations"

        self.properties = [{"name": "Mask Size",
                            "label": "masksize",
                            "type": HARPIA_COMBO,
                            "values": ["1x1", "3x3", "5x5", "7x7"]
                           }]

        # -------------------C/OpenCv code---------------------------------
        self.vars = \
            'IplImage * block$id$_img_i0 = NULL;\n' + \
            'int block$id$_int_i1 = ' + self.masksize[0] + ';\n' + \
            'int block$id$_int_i2 = ' + self.masksize[2] + ';\n' + \
            'IplImage * block$id$_img_o0 = NULL;\n' + \
            'IplConvKernel * block$id$_arg_mask = NULL;\n'

        self.function_call = \
            '\nif(block$id$_img_i0){\n' + \
            'if (block$id$_int_i1 % 2 == 0) block$id$_int_i1++;\n' + \
            'if (block$id$_int_i2 % 2 == 0) block$id$_int_i2++;\n' + \
            'block$id$_arg_mask = ' + \
            'cvCreateStructuringElementEx(block$id$_int_i1 ,' + \
            'block$id$_int_i2, 1, 1,CV_SHAPE_RECT,NULL);\n' + \
            'IplImage * block$id$_auxImg;\n' + \
            'block$id$_img_o0 = cvCloneImage(block$id$_img_i0);\n' + \
            'block$id$_auxImg = cvCloneImage(block$id$_img_i0);\n' + \
            'cvMorphologyEx(block$id$_img_i0, block$id$_img_o0, NULL,' + \
            'block$id$_arg_mask, CV_MOP_CLOSE, 1);\n}\n'

        self.dealloc = \
            'cvReleaseImage(&block$id$_img_o0);\n' + \
            'cvReleaseStructuringElement(&block$id$_arg_mask);\n' + \
            'cvReleaseImage(&block$id$_img_i0);\n'

# --------------------------------------------------------------------------
