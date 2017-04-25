#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Rotate class.
"""
from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin


class Rotate(Plugin):
    """
    This class contains methods related the Rotate class.
    """
    # -------------------------------------------------------------------------

    def __init__(self):
        Plugin.__init__(self)
        self.isCenter = True
        self.isScalling = True
        self.isFilling = True
        self.angle = 0

        # Appearance
        self.help = "Adiciona bordas na imagem."
        self.label = "Rotate Image"
        self.color = "90:5:10:150"
        self.in_types = ["harpia.extensions.c.ports.image", "harpia.extensions.c.ports.double"]
        self.out_types = ["harpia.extensions.c.ports.image"]
        self.group = "Experimental"

        self.properties = [{"name": "Use Image Center",
                            "label": "isCenter",
                            "type": HARPIA_CHECK
                            },
                           {"name": "Resize Image To Fit In",
                            "label": "isScalling",
                            "type": HARPIA_CHECK
                            },
                           {"name": "Fill Leftovers",
                            "label": "isFilling",
                            "type": HARPIA_CHECK
                            },
                           {"name": "Point X",
                            "label": "x",
                            "type": HARPIA_INT,
                            "value": 20,
                            "lower": 0,
                            "upper": 65535,
                            "step": 1
                            },
                           {"name": "Point Y",
                            "label": "y",
                            "value": 20,
                            "type": HARPIA_INT,
                            "lower": 0,
                            "upper": 65535,
                            "step": 1
                            },
                           {"name": "Angle",
                            "label": "angle",
                            "type": HARPIA_FLOAT,
                            "lower": 0,
                            "upper": 360,
                            "step": 1
                            }
                           ]

        # -------------------C/OpenCv code------------------------------------
        self.codes[1] = \
            'IplImage * block$id$_img_i0 = NULL;\n' + \
            'double block$id$_double_i1 = $angle$;\n' + \
            'IplImage * block$id$_img_o0 = NULL;\n'

        self.codes[0] = \
            "#define PI 3.1415926535898\n" + \
            "double rads(double degs){\n" + \
            "   return (PI/180 * degs);\n" + \
            "}\n\n"

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        value = \
            '\n if(block$id$_img_i0)\n  {\n' + \
            '       double scale;\n int H;\n    int W;\n' + \
            '       W = block$id$_img_i0->width;\n' + \
            '       H = block$id$_img_i0->height;\n' + \
            '       block$id$_img_o0 = cvCreateImage(cvSize(W,H),' + \
            'block$id$_img_i0->depth,block$id$_img_i0->nChannels);\n' + \
            '       CvMat* mat = cvCreateMat(2,3,CV_32FC1);\n'
        if self.isCenter == "true":
            value += '      CvPoint2D32f center = cvPoint2D32f(W/2, H/2);\n'
        else:
            value += '      CvPoint2D32f center = cvPoint2D32f($props[x]$,$props[y]$);\n'

        if self.isScalling == "true":
            value += '      scale = H/(fabs(H*sin(rads' + \
                '(90-abs(block$id$_double_i1)))) + ' + \
                'fabs(W*sin(rads(abs(block$id$_double_i1)))));\n' + \
                '       cv2DRotationMatrix' + \
                '(center,block$id$_double_i1,scale,mat);\n'
        else:
            value += '      cv2DRotationMatrix' + \
                '(center,block$id$_double_i1,1.0,mat);\n'

        if self.isFilling == "true":
            value += '      cvWarpAffine(block$id$_img_i0, ' + \
                'block$id$_img_o0, mat, ' + \
                'CV_WARP_FILL_OUTLIERS, cvScalarAll(0));\n'
        else:
            value += '      cvWarpAffine(block$id$_img_i0,' + \
                'block$id$_img_o0,mat,0,cvScalarAll(0));\n'

        value += '  }\n'
        return value


        self.language = "c"
        self.framework = "opencv"
# -----------------------------------------------------------------------------
