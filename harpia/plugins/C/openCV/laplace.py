#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Laplace class.
"""
from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class Laplace(OpenCVPlugin):
    """
    This class contains methods related the laplace class.
    """
    # -------------------------------------------------------------------------

    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.masksize = "3"

        # Appearance
        self.help = "Operação de filtragem que calcula o " + \
            "Laplaciano de uma imagem," + \
            "realçando cantos e bordas de objetos."
        self.label = "Laplace"
        self.icon = "images/laplace.png"
        self.color = "250:180:80:150"
        self.in_types = ["HRP_IMAGE", "HRP_INT"]
        self.out_types = ["HRP_IMAGE"]
        self.group = "Gradients, Edges and Corners"

        self.properties = [{"name": "Mask Size",
                            "label": "masksize",
                            "type": HARPIA_COMBO,
                            "values": ["1", "3", "5", "7", "9", "11", "13"]
                            }
                           ]

        # ------------------------------C/OpenCv code--------------------------
        self.vars = \
            'IplImage * block$id$_img_i0 = NULL; //Laplace In \n' + \
            'IplImage * block$id$_img_o0 = NULL; //Laplace Out \n' + \
            'int block$id$_int_i1 = $masksize$; // Laplace Mask Size\n'

        self.function_call = \
            '\nif(block$id$_img_i0){\n' + \
            'block$id$_int_i1 = (block$id$_int_i1 > 31)? 31 : ' + \
            'block$id$_int_i1; // Laplace Mask Constraint\n' + \
            'block$id$_int_i1 = (block$id$_int_i1 % 2 == 0)? ' + \
            'block$id$_int_i1 + 1 : block$id$_int_i1; // Only Odd\n' + \
            'CvSize size$id$ = cvGetSize(block$id$_img_i0);\n' + \
            'block$id$_img_o0 = cvCreateImage' + \
            '(size$id$, IPL_DEPTH_32F,block$id$_img_i0->nChannels);\n' + \
            'cvLaplace(block$id$_img_i0, block$id$_img_o0, ' + \
            'block$id$_int_i1);}\n'

    # ----------------------------------------------------------------------
    def generate_vars(self):
        self.masksize = int(self.masksize)
        return self.vars

# ------------------------------------------------------------------------------
