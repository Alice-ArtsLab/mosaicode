#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class Exp(OpenCVPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)

        # Appearance
        self.help = "Aplica a função exponencial a uma imagem, ou seja, " + \
            "eleva a constante neperiana ao valor " + \
            "de intensidade luminosa de cada ponto da imagem."
        self.label = "Exp"
        self.icon = "images/exp.png"
        self.color = "230:230:60:150"
        self.in_types = ["HRP_IMAGE"]
        self.out_types = ["HRP_IMAGE"]
        self.group = "Math Functions"

        # --------------------------C/OpenCv code------------------------------
        self.vars = \
            'IplImage * block$id$_img_i0 = NULL;\n' + \
            'IplImage * block$id$_img_o0 = NULL;\n' + \
            'IplImage * block$id$_img_t = NULL;\n'

        self.function_call = \
            '\nif(block$id$_img_i0){\n' + \
            'block$id$_img_t = cvCreateImage' + \
            '(cvGetSize(block$id$_img_i0), IPL_DEPTH_32F,' + \
            'block$id$_img_i0->nChannels);\n' + \
            'block$id$_img_o0 = cvCloneImage' + \
            '(block$id$_img_i0);\n' + \
            'cvConvertScale(block$id$_img_i0, ' + \
            'block$id$_img_t,(1/255.0),0);\n' + \
            'cvExp(block$id$_img_t, block$id$_img_t);\n' + \
            'cvConvertScale(block$id$_img_t, block$id$_img_o0,' + \
            ' (double)93.8092,0);\n}\n'

        self.dealloc = \
            'cvReleaseImage(&block$id$_img_o0);\n' + \
            'cvReleaseImage(&block$id$_img_i0);\n' + \
            'cvReleaseImage(&block$id$_img_t);\n'

# -----------------------------------------------------------------------------
