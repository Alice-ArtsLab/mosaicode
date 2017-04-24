#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Dilate class.
"""
from harpia.GUI.fieldtypes import *
from harpia.extensions.c.opencv.opencvplugin import OpenCVPlugin


class Dilate(OpenCVPlugin):
    """
    This class contains methods related the Dilate class.
    """

    # -------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        # Appearance
        self.help = "Operação morfológica que provoca dilatação " + \
            "nos objetos de uma imagem, aumentando suas dimensões."
        self.label = "Dilate"
        self.color = "180:230:220:150"
        self.in_ports = [{"type":"harpia.extensions.c.ports.image",
                          "name":"input_image",
                          "label":"Input Image"}
                         ]
        self.out_ports = [{"type":"harpia.extensions.c.ports.image",
                           "name":"output_image",
                           "label":"Output Image"}]
        self.group = "Morphological Operations"

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
                            },
                           {"label": "Iterations",
                            "name": "iterations",
                            "type": HARPIA_INT,
                            "lower": 0,
                            "upper": 65535,
                            "step": 1, 
                            "value":1
                            }
                           ]

        # ----------------------------C/OpenCv code---------------------------
        self.codes[1] = \
            'IplImage * block$id$_img_i0 = NULL;\n' + \
            'IplImage * block$id$_img_o0 = NULL;\n' + \
            'int block$id$_arg_iterations = $iterations$;\n' + \
            'IplConvKernel * block$id$_arg_mask = ' + \
            'cvCreateStructuringElementEx($masksizex$ , $masksizey$, 1, 1,CV_SHAPE_RECT,NULL);\n'

        self.codes[2] = '''
            if(block$id$_img_i0){
                block$id$_img_o0 = cvCloneImage(block$id$_img_i0);
                cvDilate(block$id$_img_i0,
                        block$id$_img_o0,
                        block$id$_arg_mask,
                        block$id$_arg_iterations);
            }
            '''
        self.codes[3] = "cvReleaseImage(&block$id$_img_i0);\n" + \
                       "cvReleaseImage(&block$id$_img_o0);\n"


# -----------------------------------------------------------------------------
