#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class ColorConversion(OpenCVPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.conversion_type = 'RGB -> GRAY'

        self.help = "Realiza a conversão de cores entre diferentes " + \
            "padrões de imagens coloridas e tons de cinza."

        self.description = {
            "Label": "Color Conversion",
            "Icon": "images/colorConversion.png",
            "Color": "50:125:50:150",
            "InTypes": {0: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "TreeGroup": "Filters and Color Conversion"
        }

        self.properties = {
            "conversion_type": {"name": "Conversion Type",
                                "type": HARPIA_COMBO,
                                "values": ["RGB -> GRAY",
                                           "RGB -> YCrCb",
                                           "YCrCb -> RGB",
                                           "RGB -> HSV",
                                           "HSV -> RGB",
                                           "RGB -> HLS",
                                           "HLS -> RGB",
                                           "RGB -> CIE.XYZ",
                                           "CIE.XYZ -> RGB",
                                           "RGB -> CIE.LAB",
                                           "CIE.LAB -> RGB",
                                           "RGB -> CIE.LUV",
                                           "CIE.LUV -> RGB"]
                                }
        }

        self.vars =  \
            'IplImage * block$id$_img_i0 = NULL;\n' + \
            'IplImage * block$id$_img_o0 = NULL;\n' + \
            'IplImage * block$id$_img_t = NULL;\n'

        self.function_call = ""

        self.dealloc = \
            'cvReleaseImage(&block$id$_img_t);\n' + \
            'cvReleaseImage(&block$id$_img_i0);\n' + \
            'cvReleaseImage(&block$id$_img_o0);\n'

    # ----------------------------------------------------------------------
    def get_help(self):
        return self.help

    # ----------------------------------------------------------------------
    def generate_dealloc(self):
        return self.dealloc

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
        channels = '3'
        if self.conversion_type == 'RGB -> GRAY':
            code = 'CV_RGB2GRAY'
            channels = '1'
        elif self.conversion_type == 'RGB -> YCrCb':
            code = 'CV_RGB2YCrCb'
        elif self.conversion_type == 'YCrCb -> RGB':
            code = 'CV_YCrCb2RGB'
        elif self.conversion_type == 'RGB -> HSV':
            code = 'CV_RGB2HSV'
        elif self.conversion_type == 'HSV -> RGB':
            code = 'CV_HSV2RGB'
        elif self.conversion_type == 'RGB -> HLS':
            code = 'CV_RGB2HLS'
        elif self.conversion_type == 'HLS -> RGB':
            code = 'CV_HLS2RGB'
        elif self.conversion_type == 'RGB -> CIE.XYZ':
            code = 'CV_RGB2XYZ'
        elif self.conversion_type == 'CIE.XYZ -> RGB':
            code = 'CV_XYZ2RGB'
        elif self.conversion_type == 'RGB -> CIE.LAB':
            code = 'CV_RGB2Lab'
        elif self.conversion_type == 'CIE.LAB -> RGB':
            code = 'CV_Lab2RGB'
        elif self.conversion_type == 'RGB -> CIE.LUV':
            code = 'CV_RGB2Luv'
        elif self.conversion_type == 'CIE.LUV -> RGB':
            code = 'CV_Luv2RGB'

        return \
            '\nif(block$id$_img_i0){\n' + \
            'block$id$_img_o0 = cvCloneImage' + \
            '(block$id$_img_i0);\n' + \
            'block$id$_img_t = cvCreateImage(cvGetSize(block$id$_img_i0),' + \
            'block$id$_img_i0->depth,' + channels + ');\n' + \
            'cvCvtColor(block$id$_img_i0, ' + \
            'block$id$_img_t ,' + code + ' );}\n' + \
            'if ( ' + code + ' == ' + "CV_RGB2GRAY" + ')\n' + \
            '{    cvMerge(block$id$_img_t ,block$id$_img_t ,' + \
            'block$id$_img_t ,NULL ,block$id$_img_o0);\n }\n' + \
            'else\n' + '{ block$id$_img_o0 = cvCloneImage(block$id$_img_t);\n}'


# -----------------------------------------------------------------------------
