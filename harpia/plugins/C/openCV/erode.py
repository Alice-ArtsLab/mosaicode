#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Erode class.
"""
from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class Erode(OpenCVPlugin):
    """
    This class contains methods related the Erode class.
    """

    # -------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.masksize = "3x3"
        self.iterations = 1

        # Appearance
        self.help = "Operação morfológica que provoca erosão " + \
            "nos objetos de uma imagem, reduzindo suas dimensões."
        self.label = "Erosion"
        self.color = "180:230:220:150"
        self.in_types = ["HRP_IMAGE", "HRP_INT"]
        self.out_types = ["HRP_IMAGE"]
        self.group = "Morphological Operations"

        self.properties = [{"name": "Mask Size",
                            "label": "masksize",
                            "type": HARPIA_COMBO,
                            "values": ["1x1", "3x3", "5x5", "7x7"]
                            },
                           {"name": "Iterations",
                            "label": "iterations",
                            "type": HARPIA_INT,
                            "lower": 0,
                            "upper": 65535,
                            "step": 1
                            }
                           ]

        # --------------------------C/OpenCv code------------------------------
        self.vars = \
            'IplImage * block$id$_img_i0 = NULL; // ERODE input\n' + \
            'int block$id$_int_i1 = $iterations$; // ERODE iterarions\n' + \
            'IplImage * block$id$_img_o0 = NULL; // ERODE output\n' + \
            'IplConvKernel * block$id$_arg_mask = ' + \
            'cvCreateStructuringElementEx(' + self.masksize[0] + \
            ' , ' + self.masksize[2] + ', 1, 1,CV_SHAPE_RECT,NULL);\n'

        self.function_call = \
            '\nif(block$id$_img_i0){\n' + \
            'block$id$_img_o0 = cvCloneImage(block$id$_img_i0);\n' + \
            'cvErode(block$id$_img_i0, block$id$_img_o0, ' + \
            'block$id$_arg_mask, block$id$_int_i1);\n' + \
            '}\n'

# -----------------------------------------------------------------------------
