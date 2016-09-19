#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class Threshold(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)
        self.id = -1
        self.type = self.__class__.__module__
        self.threshold = 122
        self.maxValue = 255
        self.thresholdType = "CV_THRESH_BINARY"

    # ----------------------------------------------------------------------
    def get_help(self):
        return "Operador de binarização da imagem, de acordo com um valor fixo de intensidade luminosa (valor de limiar)."

    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):
        blockTemplate.imagesIO = \
            'IplImage * block$id$_img_i1 = NULL;\n' + \
            'IplImage * block$id$_img_o1 = NULL;\n'
        blockTemplate.imagesIO += \
            'int block$id$_arg_threshold = $threshold$;\n' + \
            'int block$id$_arg_maxValue = $maxValue$;\n' + \
            'int block$id$_arg_thresholdType = $thresholdType$;\n'
        blockTemplate.functionCall = '\nif(block$id$_img_i1){\n' + \
            'block$id$_img_o1 = cvCreateImage(cvSize(block$id$' + \
            '_img_i1->width,block$id$_img_i1->height),block$id$' + \
            '_img_i1->depth,block$id$_img_i1->nChannels);\n' + \
            '\ncvThreshold(block$id$_img_i1,block$id$' + \
            '_img_o1,block$id$_arg_threshold,block$id$' + \
            '_arg_maxValue,block$id$_arg_thresholdType);}\n'
        blockTemplate.dealloc = 'cvReleaseImage(&block$id$_img_o1);\n' + \
                                'cvReleaseImage(&block$id$_img_i1);\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            "Label": _("Threshold"),
            "Icon": "images/threshold.png",
            "Color": "50:125:50:150",
            "InTypes": {0: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "Description": _("Image binarization operator, according to a fixed threshold value."),
            "TreeGroup": _("Filters and Color Conversion")
            }
    # ----------------------------------------------------------------------
    def get_properties(self):
        return {

            "threshold":{"name": "Threshold",
                    "type": HARPIA_INT,
                    "value": self.threshold,
                    "lower":0,
                    "upper":255,
                    "step":1
                    },

            "maxValue":{"name": "Max Gray Value",
                    "type": HARPIA_INT,
                    "value": self.maxValue,
                    "lower":0,
                    "upper":255,
                    "step":1
                    },

        "thresholdType":{"name": "Threshold Type",
                    "type": HARPIA_COMBO,
                    "value": self.thresholdType,
                    "values": ["CV_THRESH_BINARY", "CV_THRESH_BINARY_INV",
                            "CV_THRESH_TRUNC", "CV_THRESH_TOZERO",
                            "CV_THRESH_TOZERO_INV"]
                    }


        }
# ------------------------------------------------------------------------------
