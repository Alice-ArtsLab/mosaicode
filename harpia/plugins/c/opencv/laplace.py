#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Laplace class.
"""
from harpia.GUI.fieldtypes import *
from harpia.plugins.c.opencv.opencvplugin import OpenCVPlugin


class Laplace(OpenCVPlugin):
    """
    This class contains methods related the laplace class.
    """
    # -------------------------------------------------------------------------

    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.help = "Operação de filtragem que calcula o " + \
            "Laplaciano de uma imagem," + \
            "realçando cantos e bordas de objetos."
        self.label = "Laplace"
        self.color = "250:180:80:150"
        self.in_ports = [{"type":"HRP_IMAGE",
                          "name":"input_image",
                          "label":"Input Image"},
                          {"type":"HRP_INT",
                          "name":"masksize",
                          "label":"Mask Size"}
                         ]
        self.out_ports = [{"type":"HRP_IMAGE",
                           "name":"output_image",
                           "label":"Output Image"}]
        self.group = "Gradients, Edges and Corners"

        self.properties = [{"label": "Mask Size",
                            "name": "masksize",
                            "type": HARPIA_COMBO,
                            "value":3,
                            "values": ["1", "3", "5", "7", "9", "11", "13"]
                            }
                           ]

        # ------------------------------C/OpenCv code--------------------------
        self.codes[1] = \
            'IplImage * block$id$_img_i0 = NULL; //Laplace In \n' + \
            'IplImage * block$id$_img_o0 = NULL; //Laplace Out \n' + \
            'int block$id$_int_i1 = $prop[masksize]$; // Laplace Mask Size\n'

        self.codes[2] = \
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

# ------------------------------------------------------------------------------
