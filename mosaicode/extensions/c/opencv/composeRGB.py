#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the ComposeRGB class.
"""
from mosaicode.GUI.fieldtypes import *
from mosaicode.model.plugin import Plugin


class ComposeRGB(Plugin):
    """
    This class contains methods related the ComposeRGB class.
    """

    # -------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)

        # Appearance
        self.help = "BLOCO Composição RGB"
        self.label = "Compose RGB"
        self.color = "50:125:50:150"
        self.in_types = ["mosaicode.extensions.c.ports.image", "mosaicode.extensions.c.ports.image", "mosaicode.extensions.c.ports.image"]
        self.out_types = ["mosaicode.extensions.c.ports.image"]
        self.group = "Filters and Color Conversion"

        # ------------------------C/OpenCv code-------------------------------
        self.codes[1] = \
            'IplImage * block$id$_img_i0 = NULL;\n' + \
            'IplImage * block$id$_img_i1 = NULL;\n' + \
            'IplImage * block$id$_img_i2 = NULL;\n' + \
            'IplImage * block$id$_img_t0 = NULL;\n' + \
            'IplImage * block$id$_img_t1 = NULL;\n' + \
            'IplImage * block$id$_img_t2 = NULL;\n' + \
            'IplImage * block$id$_img_o0 = NULL;\n'

        self.codes[2] = \
            '\nif(block$id$_img_i0){\n' + \
            'block$id$_img_o0 = cvCloneImage(block$id$_img_i0);\n' + \
            'CvSize size$id$ = cvSize' + \
            '(block$id$_img_i0->width,block$id$_img_i0->height);\n' + \
            'block$id$_img_t0 = cvCreateImage' + \
            '(size$id$, block$id$_img_i0->depth, 1);\n' +\
            'block$id$_img_t1 = cvCreateImage' + \
            '(size$id$, block$id$_img_i0->depth, 1);\n' +\
            'block$id$_img_t2 = cvCreateImage' + \
            '(size$id$, block$id$_img_i0->depth, 1);\n' +\
            'cvSplit(block$id$_img_i0 ,' + \
            'block$id$_img_t0  ,NULL, NULL , NULL);\n' + \
            'cvSplit(block$id$_img_i1 ,' + \
            'NULL ,block$id$_img_t1, NULL, NULL);\n' + \
            'cvSplit(block$id$_img_i2 ,' + \
            'NULL ,NULL, block$id$_img_t2 , NULL);\n' + \
            'cvMerge(block$id$_img_t2 ,block$id$_img_t1 ,' + \
            'block$id$_img_t0 , NULL, block$id$_img_o0);}\n'

        self.codes[3] = \
            'cvReleaseImage(&block$id$_img_t0);\n' + \
            'cvReleaseImage(&block$id$_img_t1);\n' + \
            'cvReleaseImage(&block$id$_img_t2);\n' + \
            'cvReleaseImage(&block$id$_img_o0);\n' + \
            'cvReleaseImage(&block$id$_img_i0);\n' + \
            'cvReleaseImage(&block$id$_img_i1);\n' + \
            'cvReleaseImage(&block$id$_img_i2);\n'


        self.language = "c"
        self.framework = "opencv"
# -----------------------------------------------------------------------------
