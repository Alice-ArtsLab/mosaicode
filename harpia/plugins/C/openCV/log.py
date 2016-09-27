#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin

class Log(OpenCVPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "aplica a função logarítmica a uma imagem, ou seja,\
        calcula o logarítmo natural do valor de intensidade luminosa de cada ponto da imagem."

    # ----------------------------------------------------------------------
    def generate_vars(self):
        return \
            'IplImage * block$id$_img_i0 = NULL;\n' + \
            'IplImage * block$id$_img_o0 = NULL;\n' + \
            'IplImage * block$id$_img_t = NULL;\n'

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return \
            '\nif(block$id$_img_i0){\n' + \
            'block$id$_img_t = cvCreateImage(cvGetSize(block$id$_img_i0), IPL_DEPTH_32F,block$id$_img_i0->nChannels);\n' + \
            'block$id$_img_o0 = cvCloneImage(block$id$_img_i0);\n' + \
            'cvConvertScale(block$id$_img_i0, block$id$_img_t,(1/93.8092),0);\n' + \
            'cvLog(block$id$_img_t, block$id$_img_t);\n' + \
            'cvConvertScale(block$id$_img_t,block$id$_img_o0,255.0,0);}\n'

    # ----------------------------------------------------------------------
    def generate_dealloc(self):
        return 'cvReleaseImage(&block$id$_img_o0);\n' + \
               'cvReleaseImage(&block$id$_img_i0);\n' + \
               'cvReleaseImage(&block$id$_img_t);\n'


    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Label": "Log",
            "Icon": "images/log.png",
            "Color": "230:230:60:150",
            "InTypes": {0: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "TreeGroup": "Math Functions"
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {}

# ------------------------------------------------------------------------------

