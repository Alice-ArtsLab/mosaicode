#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Log class.
"""
from harpia.GUI.fieldtypes import *
from harpia.plugins.c.opencv.opencvplugin import OpenCVPlugin


class Log(OpenCVPlugin):
    """
    This class contains methods related the Log class.
    """
    # -------------------------------------------------------------------------

    def __init__(self):
        OpenCVPlugin.__init__(self)

        # Appearance
        self.help = "Aplica a função logarítmica a uma imagem, ou seja," + \
            "calcula o logarítmo natural do valor de intensidade" + \
            " luminosa de cada ponto da imagem."
        self.label = "Log"
        self.color = "230:230:60:150"
        self.in_ports = [{"type":"HRP_IMAGE",
                          "name":"input_image",
                          "label":"Input Image"}
                         ]
        self.out_ports = [{"type":"HRP_IMAGE",
                           "name":"output_image",
                           "label":"Output Image"}]
        self.group = "Math Functions"

        # ------------------------------C/OpenCv code--------------------------
        self.codes[1] = \
            'IplImage * block$id$_img_i0 = NULL;\n' + \
            'IplImage * block$id$_img_o0 = NULL;\n' + \
            'IplImage * block$id$_img_t = NULL;\n'

        self.codes[2] = \
            '\nif(block$id$_img_i0){\n' + \
            'block$id$_img_t = cvCreateImage(cvGetSize' + \
            '(block$id$_img_i0), IPL_DEPTH_32F,' + \
            'block$id$_img_i0->nChannels);\n' + \
            'block$id$_img_o0 = cvCloneImage(block$id$_img_i0);\n' + \
            'cvConvertScale(block$id$_img_i0, ' + \
            'block$id$_img_t,(1/93.8092),0);\n' + \
            'cvLog(block$id$_img_t, block$id$_img_t);\n' + \
            'cvConvertScale(block$id$_img_t,block$id$_img_o0,255.0,0);}\n'

        self.codes[3] = \
            'cvReleaseImage(&block$id$_img_o0);\n' + \
            'cvReleaseImage(&block$id$_img_i0);\n' + \
            'cvReleaseImage(&block$id$_img_t);\n'

# -----------------------------------------------------------------------------
