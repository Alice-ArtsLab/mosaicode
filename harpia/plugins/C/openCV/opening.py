#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class Opening(OpenCVPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.masksize = "3x3"

        self.help = "Operação morfológica que visa " + \
            "desconectar objetos em uma imagem ou suprimir ruídos."

        self.description = {
            "Label": "Opening",
            "Icon": "images/opening.png",
            "Color": "180:230:220:150",
            "InTypes": {0: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "TreeGroup": "Morphological Operations"
        }

        self.properties = {
            "masksize": {
                "name": "Mask Size",
                "type": HARPIA_COMBO,
                "values": ["1x1", "3x3", "5x5", "7x7"]
            }
        }

        # -------------------C/OpenCv code------------------------------------
        self.vars = \
            'IplImage * block$id$_img_i0 = NULL;\n' + \
            'IplImage * block$id$_img_o0 = NULL;\n' + \
            'IplConvKernel * block$id$' + \
            '_arg_mask = cvCreateStructuringElementEx(' + \
            self.masksize[0] + ' , ' + \
            self.masksize[2] + ', 1, 1,CV_SHAPE_RECT,NULL);\n'

        self.function_call = \
            '\nif(block$id$_img_i0){\n' + \
            'IplImage * block$id$_auxImg;' + \
            'block$id$_img_o0 = cvCloneImage(block$id$_img_i0);\n' + \
            'block$id$_auxImg = cvCloneImage(block$id$_img_i0);\n' + \
            'cvMorphologyEx(block$id$_img_i0, block$id$_img_o0, NULL,' + \
            'block$id$_arg_mask, CV_MOP_OPEN, 1);\n}\n'

        self.dealloc = \
            'cvReleaseImage(&block$id$_img_o0);\n' + \
            'cvReleaseStructuringElement(&block$id$_arg_mask);\n' + \
            'cvReleaseImage(&block$id$_img_i0);\n'

    # ----------------------------------------------------------------------
    def get_help(self):
        return self.help

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

# -----------------------------------------------------------------------------
