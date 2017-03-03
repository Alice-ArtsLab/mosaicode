#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the CropImage class.
"""

from harpia.GUI.fieldtypes import *
from harpia.plugins.c.opencv.opencvplugin import OpenCVPlugin


class CropImage(OpenCVPlugin):
    """
    This class contains methods related the CropImage class.
    """

    # -------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.x0 = 0
        self.y0 = 0
        self.width = 640
        self.height = 480

        # Appearance
        self.help = "Corta a Imagem de acordo com o Retangulo de entrada."
        self.label = "Crop Image"
        self.color = "50:50:200:150"
        self.in_types = ["HRP_IMAGE", "HRP_RECT"]
        self.out_types = ["HRP_IMAGE"]
        self.group = "Experimental"

        self.properties = [{"name": "X",
                            "label": "x0",
                            "type": HARPIA_INT,
                            "lower": 1,
                            "upper": 65535,
                            "step": 1
                            },
                           {"name": "Y",
                            "label": "y0",
                            "type": HARPIA_INT,
                            "lower": 1,
                            "upper": 65535,
                            "step": 1
                            },
                           {"name": "Width",
                            "label": "width",
                            "type": HARPIA_INT,
                            "lower": 1,
                            "upper": 65535,
                            "step": 1
                            },
                           {"name": "Height",
                            "label": "height",
                            "type": HARPIA_INT,
                            "lower": 1,
                            "upper": 65535,
                            "step": 1
                            }
                           ]

        # ------------------------C/OpenCv code--------------------------------
        self.vars = \
            'IplImage * block$id$_img_i0 = NULL;\n' + \
            'IplImage * block$id$_img_o0 = NULL;\n' + \
            'CvRect  block$id$_rect_i1 = cvRect' + \
            '($x0$, $y0$, $width$, $height$);\n'

        self.function_call = \
            '\nif(block$id$_img_i0){\n' + \
            '   block$id$_rect_i1.x = MAX' + \
            '(0,block$id$_rect_i1.x);//Check whether point is negative\n' + \
            '   block$id$_rect_i1.y = MAX' + \
            '(0,block$id$_rect_i1.y);\n' + \
            '   block$id$_rect_i1.x = MIN(block$id$_img_i0->width-1,' + \
            'block$id$_rect_i1.x);//Check whether ' + \
            'point is out of the image\n' + \
            '   block$id$_rect_i1.y = MIN' + \
            '(block$id$_img_i0->height-1,' + \
            'block$id$_rect_i1.y);\n' + \
            '   block$id$_rect_i1.width = MIN' + \
            '(block$id$_img_i0->width-block$id$_rect_i1.x,' + \
            'block$id$_rect_i1.width);' + \
            '//Check whether rect reaches out of the image\n' + \
            '   block$id$_rect_i1.height = MIN(block$id$_img_i0->' + \
            'height-block$id$_rect_i1.y,block$id$_rect_i1.height);\n' + \
            '   block$id$_img_o0 = cvCreateImage' + \
            '(cvSize(block$id$_rect_i1.width,' + \
            'block$id$_rect_i1.height),' + \
            ' block$id$_img_i0->depth,block$id$_img_i0->nChannels);\n' + \
            '   cvSetImageROI(block$id$_img_i0,block$id$_rect_i1);\n' + \
            '   cvCopyImage(block$id$_img_i0,block$id$_img_o0);\n' + \
            '}\n'

# ------------------------------------------------------------------------------
