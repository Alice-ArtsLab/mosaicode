#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class UpToBottom(OpenCVPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)

        # Appearance
        self.help = "Coloca uma imagem debaixo da outra."
        self.label = "Up to Bottom"
        self.icon = "images/and.png"
        self.color = "10:180:10:150"
        self.in_types = ["HRP_IMAGE", "HRP_IMAGE"]
        self.out_types = ["HRP_IMAGE"]
        self.group = "Arithmetic and logical operations"

        # -------------------C/OpenCv code------------------------------------
        self.function_call = \
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

        self.dealloc = \
            'if (block$id$_img_o0) cvReleaseImage(&block$id$_img_o0);\n' + \
            'cvReleaseImage(&block$id$_img_i0);\n' + \
            'cvReleaseImage(&block$id$_img_i1);\n'

# -----------------------------------------------------------------------------
