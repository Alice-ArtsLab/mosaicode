#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin

class EqualizeHistogram(OpenCVPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)

    # ----------------------------------------------------------------------
    def get_help(self):
        return "a equalização do histograma de uma imagem visa alcançar maior contraste entre os diversos elementos de uma imagem."

    # ----------------------------------------------------------------------
    def generate_vars(self):
        return \
            'IplImage * block$id$_img_i0 = NULL;\n' + \
            'IplImage * block$id$_img_o0 = NULL;\n' + \
            'IplImage * block$id$_SourceCx[3];\n' + \
            'IplImage * block$id$_EqCx[3];\n'

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return \
            '\nif(block$id$_img_i0){\n' + \
            'CvSize size$id$ = cvGetSize(block$id$_img_i0);\n'+ \
            'block$id$_img_o0 = cvCreateImage(size$id$, IPL_DEPTH_8U, 3);\n' + \
            'block$id$_SourceCx[0] = cvCreateImage(size$id$, IPL_DEPTH_8U, 1);\n' + \
            'block$id$_SourceCx[1] = cvCreateImage(size$id$, IPL_DEPTH_8U, 1);\n' + \
            'block$id$_SourceCx[2] = cvCreateImage(size$id$, IPL_DEPTH_8U, 1);\n' + \
            'block$id$_EqCx[0] = cvCreateImage(size$id$, IPL_DEPTH_8U, 1);\n' + \
            'block$id$_EqCx[1] = cvCreateImage(size$id$, IPL_DEPTH_8U, 1);\n' + \
            'block$id$_EqCx[2] = cvCreateImage(size$id$, IPL_DEPTH_8U, 1);\n' + \
            'cvSplit(block$id$_img_i0, block$id$_SourceCx[0],' + \
            'block$id$_SourceCx[1],block$id$_SourceCx[2], NULL);\n' + \
            'cvEqualizeHist(block$id$_SourceCx[0], block$id$_EqCx[0]);\n' + \
            'cvEqualizeHist(block$id$_SourceCx[1], block$id$_EqCx[1]);\n' + \
            'cvEqualizeHist(block$id$_SourceCx[2], block$id$_EqCx[2]);\n' + \
            'cvMerge( block$id$_EqCx[0],block$id$_EqCx[1],' + \
            'block$id$_EqCx[2], NULL,block$id$_img_o0);\n' + \
            'cvReleaseImage(&block$id$_SourceCx[0]);\n' + \
            'cvReleaseImage(&block$id$_SourceCx[1]);\n' + \
            'cvReleaseImage(&block$id$_SourceCx[2]);\n' + \
            'cvReleaseImage(&block$id$_EqCx[0]);\n' + \
            'cvReleaseImage(&block$id$_EqCx[1]);\n' + \
            'cvReleaseImage(&block$id$_EqCx[2]);\n' + \
            '}\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Label": "Equalize Histogram",
            "Icon": "images/equalizeHistogram.png",
            "Color": "0:0:0:150",
            "InTypes": {0: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "TreeGroup": "Histograms"
            }
    # ----------------------------------------------------------------------
    def get_properties(self):
        return {}

# ------------------------------------------------------------------------------

