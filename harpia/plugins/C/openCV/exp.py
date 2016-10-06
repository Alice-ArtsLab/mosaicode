#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin

class Exp(OpenCVPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)

        self.help = "Aplica a função exponencial a uma imagem, ou seja, " + \
        "eleva a constante neperiana ao valor de intensidade luminosa de cada ponto da imagem."

        self.description = {
            "Label":"Exp",
            "Icon":"images/exp.png",
            "Color":"230:230:60:150",
            "InTypes":{0:"HRP_IMAGE"},
            "OutTypes":{0:"HRP_IMAGE"},
            "TreeGroup":"Math Functions"
        }

        self.properties = {}

        #--------------------------C/OpenCv code-------------------------------
        self.vars = \
           'IplImage * block$id$_img_i0 = NULL;\n' + \
           'IplImage * block$id$_img_o0 = NULL;\n' + \
           'IplImage * block$id$_img_t = NULL;\n'

        self.function_call = \
            '\nif(block$id$_img_i0){\n' + \
            'block$id$_img_t = cvCreateImage(cvGetSize(block$id$_img_i0), IPL_DEPTH_32F,block$id$_img_i0->nChannels);\n'+\
            'block$id$_img_o0 = cvCloneImage(block$id$_img_i0);\n' + \
            'cvConvertScale(block$id$_img_i0, block$id$_img_t,(1/255.0),0);\n' + \
            'cvExp(block$id$_img_t, block$id$_img_t);\n' + \
            'cvConvertScale(block$id$_img_t, block$id$_img_o0, (double)93.8092,0);\n}\n'

        self.dealloc = \
            'cvReleaseImage(&block$id$_img_o0);\n' + \
            'cvReleaseImage(&block$id$_img_i0);\n' + \
            'cvReleaseImage(&block$id$_img_t);\n'


    # ----------------------------------------------------------------------
    def get_help(self):
      return self.help

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return self.description

    # ----------------------------------------------------------------------
    def get_properties(self):
        return self.properties

    # ----------------------------------------------------------------------
    def generate_vars(self):
        return self.vars

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return self.function_call

    # ----------------------------------------------------------------------
    def generate_dealloc(self):
        return self.dealloc
        
# ------------------------------------------------------------------------------
