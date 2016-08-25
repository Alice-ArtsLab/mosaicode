#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class Resize(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)
        self.id = -1
        self.type = "604"
        self.method = "CV_INTER_LINEAR"

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Resizes the input image to the dimensions of the input rectangle"

    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):
        blockTemplate.imagesIO = \
            'IplImage * block$$_img_i1 = NULL;\n' + \
            'IplImage * block$$_img_o1 = NULL;\n' + \
            'CvRect block$$_rect_i2;\n'
        blockTemplate.functionCall = '\nif(block$$_img_i1){\n' + \
                                     '	block$$_img_o1 = cvCreateImage(cvSize(block$$_rect_i2.width,block$$_rect_i2.height),block$$_img_i1->depth,block$$_img_i1->nChannels);\n' + \
                                     '	cvResize(block$$_img_i1, block$$_img_o1, ' + self.method + ');\n' + \
                                     '}\n'
        blockTemplate.dealloc = 'cvReleaseImage(&block$$_img_o1);\n' + \
                                'cvReleaseImage(&block$$_img_i1);\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            "Label": _("Resize Image"),
            "Icon": "images/resize.png",
            "Color": "20:80:10:150",
            "InTypes": {0: "HRP_IMAGE", 1: "HRP_RECT"},
            "OutTypes": {0: "HRP_IMAGE"},
            "Description": _("Resizes the input image to the dimensions of the input rectangle"),
            "TreeGroup": _("Experimental")
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {
        "method":{"name": "Method",
                    "type": HARPIA_COMBO,
                    "value": self.method,
                    "values": ["CV_INTER_NN", "CV_INTER_LINEAR" , "CV_INTER_AREA", "CV_INTER_CUBIC"]
                    }
        }

# ------------------------------------------------------------------------------
