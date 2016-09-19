#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class EqualizeHistogram(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)
        self.id = -1
        self.type = self.__class__.__module__

    # ----------------------------------------------------------------------
    def get_help(self):
        return "a equalização do histograma de uma imagem visa alcançar maior contraste entre os diversos elementos de uma imagem."

    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):
        blockTemplate.imagesIO = \
            'IplImage * block$id$_img_i1 = NULL;\n' + \
            'IplImage * block$id$_img_o1 = NULL;\n' + \
            'IplImage * block$id$_SourceCx[3];\n' + \
            'IplImage * block$id$_EqCx[3];\n'
        blockTemplate.functionCall = '\nif(block$id$_img_i1){\n' + \
                  'block$id$_img_o1 = cvCreateImage(cvSize(block$id$_img_i1->width,block$id$_img_i1->height), IPL_DEPTH_8U, 3);\n' + \
                  'block$id$_SourceCx[0] = cvCreateImage(cvSize(block$id$_img_i1->width,block$id$_img_i1->height), IPL_DEPTH_8U, 1);\n' + \
                  'block$id$_SourceCx[1] = cvCreateImage(cvSize(block$id$_img_i1->width,block$id$_img_i1->height), IPL_DEPTH_8U, 1);\n' + \
                  'block$id$_SourceCx[2] = cvCreateImage(cvSize(block$id$_img_i1->width,block$id$_img_i1->height), IPL_DEPTH_8U, 1);\n' + \
                  'block$id$_EqCx[0] = cvCreateImage(cvSize(block$id$_img_i1->width,block$id$_img_i1->height), IPL_DEPTH_8U, 1);\n' + \
                  'block$id$_EqCx[1] = cvCreateImage(cvSize(block$id$_img_i1->width,block$id$_img_i1->height), IPL_DEPTH_8U, 1);\n' + \
                  'block$id$_EqCx[2] = cvCreateImage(cvSize(block$id$_img_i1->width,block$id$_img_i1->height), IPL_DEPTH_8U, 1);\n' + \
                  'cvSplit(block$id$_img_i1,block$id$_SourceCx[0],' + \
                  'block$id$_SourceCx[1],block$id$_SourceCx[2], NULL);\n' + \
                  'cvEqualizeHist(block$id$_SourceCx[0], block$id$_EqCx[0]);\n' + \
                  'cvEqualizeHist(block$id$_SourceCx[1], block$id$_EqCx[1]);\n' + \
                  'cvEqualizeHist(block$id$_SourceCx[2], block$id$_EqCx[2]);\n' + \
                  'cvMerge( block$id$_EqCx[0],block$id$_EqCx[1],' + \
                  'block$id$_EqCx[2], NULL,block$id$_img_o1);\n' + \
                  'cvReleaseImage(&block$id$_SourceCx[0]);\n' + \
                  'cvReleaseImage(&block$id$_SourceCx[1]);\n' + \
                  'cvReleaseImage(&block$id$_SourceCx[2]);\n' + \
                  'cvReleaseImage(&block$id$_EqCx[0]);\n' + \
                  'cvReleaseImage(&block$id$_EqCx[1]);\n' + \
                  'cvReleaseImage(&block$id$_EqCx[2]);\n' + \
                  '}\n'
        blockTemplate.dealloc = 'cvReleaseImage(&block$id$_img_o1);\n' + \
                                'cvReleaseImage(&block$id$_img_i1);\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            "Label": _("Equalize Histogram"),
            "Icon": "images/equalizeHistogram.png",
            "Color": "0:0:0:150",
            "InTypes": {0: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "Description": _("The histogram equalization of an image intends to reinforce contrast of the image elements."),
            "TreeGroup": _("Histograms")
            }
    # ----------------------------------------------------------------------
    def get_properties(self):
        return {}

# ------------------------------------------------------------------------------

