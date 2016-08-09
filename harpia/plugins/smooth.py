#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class Smooth(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        self.id = -1
        self.type = "82"
        self.smooth_type = "CV_GAUSSIAN"
        self.param1 = 7
        self.param2 = 9

    # ----------------------------------------------------------------------
    def get_help(self):
        return "Aplicação de um filtro de suavização. Suaviza os contornos de objetos na imagem, borrando-os levemente."

    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):
        blockTemplate.imagesIO = \
            'IplImage * block$$_img_i1 = NULL;\n' + \
            'IplImage * block$$_img_o1 = NULL;\n' + \
            'IplImage * block$$_img_t = NULL;\n'
        blockTemplate.functionCall = '\nif(block$$_img_i1){\n' + \
                                     'block$$_img_o1 = cvCreateImage(cvSize(block$$_img_i1->width,block$$_img_i1->height), block$$_img_i1->depth,block$$' + \
                                     '_img_i1->nChannels);\n' + \
                                     'cvSmooth(block$$_img_i1, block$$_img_o1 ,' + self.smooth_type + ',' + str(self.param1) + ',' + str(self.param2) + ',0,0);}\n'
        blockTemplate.dealloc = 'cvReleaseImage(&block$$_img_o1);\n' + \
                                'cvReleaseImage(&block$$_img_i1);\n' + \
                                'cvReleaseImage(&block$$_img_t);\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            "Label": _("Smooth"),
            "Icon": "images/smooth.png",
            "Color": "50:125:50:150",
            "InTypes": {0: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "Description": _("Operação de filtragem destinada suavizar uma imagem"),
            "TreeGroup": _("Filters and Color Conversion")
            }
    # ----------------------------------------------------------------------
    def get_properties(self):
        return {
        "smooth_type":{"name": "Type",
                    "type": HARPIA_COMBO,
                    "value": self.smooth_type,
                    "values": ["CV_GAUSSIAN", "CV_BLUR", "CV_MEDIAN"]
                    },
        "param1":{"name": "Parameter 1",
                    "type": HARPIA_INT,
                    "value": self.param1,
                    "lower":0,
                    "upper":99,
                    "step":1
                    },
        "param2":{"name": "Parameter 2",
                    "type": HARPIA_INT,
                    "value": self.param2,
                    "lower":0,
                    "upper":99,
                    "step":1
                    }
        }

# ------------------------------------------------------------------------------
