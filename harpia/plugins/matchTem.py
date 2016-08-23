#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class MatchTem(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        self.id = -1
        self.type = "605"
        self.method = 'CV_TM_SQDIFF'
        self.scaleFactor = 6

    # ----------------------------------------------------------------------
    def get_help(self):
        return "operação de filtragem destinada a suavizar uma imagem."

    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):
        blockTemplate.imagesIO = \
            'IplImage * block$$_img_i1 = NULL;\n' + \
            'IplImage * block$$_img_i2 = NULL;\n' + \
            'IplImage * block$$_img_t1 = NULL;\n' + \
            'IplImage * block$$_img_o1 = NULL;\n'
        blockTemplate.functionCall = '\nif(block$$_img_i1 && block$$_img_i2)\n' + \
                                     '{\n' + \
                                     '	block$$_img_t1 = cvCreateImage(cvSize(block$$_img_i1->width - block$$_img_i2->width +1,block$$_img_i1->height - block$$_img_i2->height +1),32,1);\n' + \
                                     '	block$$_img_o1 = cvCreateImage(cvSize(block$$_img_i1->width - block$$_img_i2->width +1,block$$_img_i1->height - block$$_img_i2->height +1),8,1);\n' + \
                                     '	cvMatchTemplate(block$$_img_i1 , block$$_img_i2, block$$_img_t1, ' + self.method + ');\n' + \
                                     '	cvConvertScale(block$$_img_t1,block$$_img_o1, ' + str(
            10 ** -(int(float(self.scaleFactor)))) + ',0);\n' + \
                                     '}\n'
        blockTemplate.dealloc = 'cvReleaseImage(&block$$_img_o1);\n' + \
                                'cvReleaseImage(&block$$_img_t1);\n' + \
                                'cvReleaseImage(&block$$_img_i2);\n' + \
                                'cvReleaseImage(&block$$_img_i1);\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            "Label": _("Match Template"),
            "Icon": "images/matchTem.png",
            "Color": "180:180:10:150",
            "InTypes": {0: "HRP_IMAGE", 1: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "Description": _("Output shows the matching relation between image (input1) and template (input2)"),
            "TreeGroup": _("Feature Detection")
            }
    # ----------------------------------------------------------------------
    def get_properties(self):
        return {

            "scaleFactor":{"name": "Scale Factor",
                    "type": HARPIA_INT,
                    "value": self.scaleFactor,
                    "lower":0,
                    "upper":99,
                    "step":1
                    },

        "method":{"name": "Method",
                    "type": HARPIA_COMBO,
                    "value": self.method,
                    "values": ["CV_TM_CCOEFF_NORMED", "CV_TM_CCOEFF",
                                "CV_TM_CCORR_NORMED", "CV_TM_CCORR",
                                "CV_TM_SQDIFF_NORMED", "CV_TM_SQDIFF"
                    ]
                    }

        }

# ------------------------------------------------------------------------------

