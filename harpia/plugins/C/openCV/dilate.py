#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class Dilate(OpenCVPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.masksize = "3x3"
        self.iterations = 1

        # Appearance
        self.help = "Operação morfológica que provoca dilatação " + \
            "nos objetos de uma imagem, aumentando suas dimensões."
        self.label = "Dilate"
        self.icon = "images/dilate.png"
        self.color = "180:230:220:150"
        self.in_types = ["HRP_IMAGE"]
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

        # ----------------------------C/OpenCv code---------------------------
        self.vars = \
            'IplImage * block$id$_img_i0 = NULL;\n' + \
            'IplImage * block$id$_img_o0 = NULL;\n' + \
            'int block$id$_arg_iterations = $iterations$;\n' + \
            'IplConvKernel * block$id$_arg_mask = ' + \
            'cvCreateStructuringElementEx(' + \
            str(self.masksize[0]) + ' , ' + \
            str(self.masksize[2]) + ', 1, 1,CV_SHAPE_RECT,NULL);\n'

        self.function_call = '''
            if(block$id$_img_i0){
                block$id$_img_o0 = cvCloneImage(block$id$_img_i0);
                cvDilate(block$id$_img_i0,
                        block$id$_img_o0,
                        block$id$_arg_mask,
                        block$id$_arg_iterations);
            }
            '''

# -----------------------------------------------------------------------------
