#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class Erode(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)
        self.id = -1
        self.type = self.__class__.__module__
        self.masksize = "3x3"
        self.iterations = 1

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "operação morfológica que provoca erosão nos objetos de uma imagem, reduzindo suas dimensões."

    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):
        self.iterations = int(float(self.iterations))
        blockTemplate.imagesIO += \
            'IplImage * block$id$_img_i1 = NULL; // ERODE input\n' + \
            'int block$id$_int_i2 = $iterations$; // ERODE iterarions\n' + \
            'IplImage * block$id$_img_o1 = NULL; // ERODE output\n' + \
            '\n\n' + \
            'IplConvKernel * block$id$_arg_mask = cvCreateStructuringElementEx(' + self.masksize[0] + \
                    ' , ' + self.masksize[2] + ', 1, 1,CV_SHAPE_RECT,NULL);\n'

        blockTemplate.functionCall = '\nif(block$id$_img_i1){\n' + \
             'block$id$_img_o1 = cvCreateImage(cvSize(block$id$' + \
             '_img_i1->width, block$id$_img_i1->height), block$id$' + \
             '_img_i1->depth ,block$id$_img_i1->nChannels);\n' + \
             '\ncvErode(block$id$_img_i1,block$id$' + \
             '_img_o1,block$id$_arg_mask,block$id$_int_i2);\n}\n'

        blockTemplate.dealloc = 'cvReleaseImage(&block$id$_img_o1); // ERODE input\n' + \
                                'cvReleaseImage(&block$id$_img_i1); // ERODE output\n'


    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            "Label": _("Erosion"),
            "Icon": "images/erode.png",
            "Color": "180:230:220:150",
            "InTypes": {0: "HRP_IMAGE", 1: "HRP_INT"},
            "OutTypes": {0: "HRP_IMAGE"},
            "Description": _("Morphological operation that erodes the objects of the image, reducing their size."),
            "TreeGroup": _("Morphological Operations")
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {
        "masksize":{"name": "Mask Size",
                    "type": HARPIA_COMBO,
                    "value": self.masksize,
                    "values": ["1x1", "3x3", "5x5", "7x7"]
                    },
        "iterations":{"name": "Iterations",
                    "type": HARPIA_INT,
                    "value": self.iterations,
                    "lower":0,
                    "upper":65535,
                    "step":1
                    }
        }

# ------------------------------------------------------------------------------
