#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the UpToBottom class.
"""
from harpia.GUI.fieldtypes import *
from harpia.plugins.c.opencv.opencvplugin import OpenCVPlugin


class UpToBottom(OpenCVPlugin):
    """
    This class contains methods related the UpToBottom class.
    """
    # -------------------------------------------------------------------------

    def __init__(self):
        OpenCVPlugin.__init__(self)

        # Appearance
        self.help = "Coloca uma imagem debaixo da outra."
        self.label = "Up to Bottom"
        self.color = "10:180:10:150"
        self.in_ports = [{"type":"HRP_IMAGE",
                          "name":"top_image",
                          "label":"Top Image"},
                         {"type":"HRP_IMAGE",
                          "name":"bottom_image",
                          "label":"Bottom Image"}
                         ]
        self.out_ports = [{"type":"HRP_IMAGE",
                           "name":"output_image",
                           "label":"Output Image"}]
        self.group = "Arithmetic and logical operations"

        self.codes[1] = "IplImage * block$id$_img_i0 = NULL;\n" + \
                    "IplImage * block$id$_img_i1 = NULL;\n" + \
                    "IplImage * block$id$_img_o0 = NULL;\n"

        self.codes[2] = \
            'if(block$id$_img_i0 && block$id$_img_i1){\n' + \
            'int width = (block$id$_img_i0->width > ' + \
            'block$id$_img_i1->width)? block$id$_img_i0->width :' + \
            ' block$id$_img_i1->width;\n' + \
            'int height = block$id$_img_i0->height +' + \
            ' block$id$_img_i1->height;\n' + \
            'block$id$_img_o0=cvCreateImage' + \
            '(cvSize(width,height),IPL_DEPTH_8U,3); \n' + \
            'cvSetImageROI(block$id$_img_o0, cvRect(0, 0, ' + \
            'block$id$_img_i0->width, block$id$_img_i0->height) );\n' + \
            'cvCopy(block$id$_img_i0,block$id$_img_o0,NULL);\n' + \
            'cvResetImageROI(block$id$_img_o0);\n' + \
            'cvSetImageROI(block$id$_img_o0, cvRect' + \
            '(0, block$id$_img_i0->height, ' + \
            'block$id$_img_i1->width, height) );\n' + \
            'cvCopy(block$id$_img_i1,block$id$_img_o0,NULL);\n' + \
            'cvResetImageROI(block$id$_img_o0);\n' + \
            '}\n'

        self.codes[3] = \
            'if (block$id$_img_o0) cvReleaseImage(&block$id$_img_o0);\n' + \
            'cvReleaseImage(&block$id$_img_i0);\n' + \
            'cvReleaseImage(&block$id$_img_i1);\n'

# -----------------------------------------------------------------------------
