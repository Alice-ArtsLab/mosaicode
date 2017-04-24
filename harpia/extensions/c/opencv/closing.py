#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Closing class.
"""
from harpia.GUI.fieldtypes import *
from harpia.extensions.c.opencv.opencvplugin import OpenCVPlugin


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
        self.color = "180:230:220:150"
        self.group = "Morphological Operations"
        self.in_ports = [{"type":"harpia.extensions.c.ports.image",
                          "name":"input_image",
                          "label":"Input Image"},
                          {"type":"harpia.extensions.c.ports.int",
                          "name":"masksizex",
                          "label":"Mask Size X"},
                          {"type":"harpia.extensions.c.ports.int",
                          "name":"masksizey",
                          "label":"Mask Size Y"}
                         ]
        self.out_ports = [{"type":"harpia.extensions.c.ports.image",
                           "name":"output_image",
                           "label":"Output Image"}]

        self.properties = [{"label": "Mask Size X",
                            "name": "masksizex",
                            "type": HARPIA_COMBO,
                            "values": ["1", "3", "5", "7"],
                            "value":"3"
                            },
                            {"label": "Mask Size Y",
                            "name": "masksizey",
                            "type": HARPIA_COMBO,
                            "values": ["1", "3", "5", "7"],
                            "value":"3"
                            }
                            ]

        # -------------------C/OpenCv code---------------------------------
        self.codes[1] = \
            'IplImage * block$id$_img_i0 = NULL;\n' + \
            'int block$id$_int_i1 = $masksizex$;\n' + \
            'int block$id$_int_i2 = $masksizey$;\n' + \
            'IplImage * block$id$_img_o0 = NULL;\n' + \
            'IplConvKernel * block$id$_arg_mask = NULL;\n'

        self.codes[2] = \
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

        self.codes[3] = \
            'cvReleaseImage(&block$id$_img_o0);\n' + \
            'cvReleaseStructuringElement(&block$id$_arg_mask);\n' + \
            'cvReleaseImage(&block$id$_img_i0);\n'

# --------------------------------------------------------------------------
