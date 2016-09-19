#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class Closing(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)
        self.id = -1
        self.type = self.__class__.__module__
        self.masksize = "7x7"

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return"Operação de morfologia matemática para realizar a fechamento da imagem de acordo com o elemento estruturante. Equivale a aplicação de uma dilatação seguida de uma erosão."

    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):
        blockTemplate.imagesIO = \
            'IplImage * block$id$_img_i1 = NULL;\n' + \
            'int block$id$_int_i2 = ' + self.masksize[0] + ';\n' + \
            'int block$id$_int_i3 = ' + self.masksize[2] + ';\n' + \
            'IplImage * block$id$_img_o1 = NULL;\n' + \
            'IplConvKernel * block$id$_arg_mask = NULL;\n'
        blockTemplate.functionCall = '\nif(block$id$_img_i1){\n' + \
            'if (block$id$_int_i2 % 2 == 0) block$id$_int_i2++;\n' + \
            'if (block$id$_int_i3 % 2 == 0) block$id$_int_i3++;\n' + \
            'block$id$_arg_mask = ' + \
            'cvCreateStructuringElementEx(block$id$_int_i2 ,' + \
            'block$id$_int_i3, 1, 1,CV_SHAPE_RECT,NULL);\n' + \
            'IplImage * block$id$_auxImg;\n' + \
            'block$id$_img_o1 = cvCreateImage(cvSize(block$id$' +\
            '_img_i1->width, block$id$_img_i1->height), block$id$' +\
            '_img_i1->depth ,block$id$_img_i1->nChannels);\n' + \
            '\nblock$id$_auxImg = cvCreateImage(cvSize(block$id$' +\
            '_img_i1->width, block$id$_img_i1->height), block$id$' +\
            '_img_i1->depth ,block$id$_img_i1->nChannels);\n' + \
            'cvMorphologyEx(block$id$_img_i1,block$id$_img_o1,NULL,' + \
            'block$id$_arg_mask, CV_MOP_CLOSE, 1);\n}\n'
        blockTemplate.dealloc = 'cvReleaseImage(&block$id$_img_o1);\n' + \
                                'cvReleaseStructuringElement(&block$id$_arg_mask);\n' + \
                                'cvReleaseImage(&block$id$_img_i1);\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            "Label": _("Closing"),
            "Icon": "images/closing.png",
            "Color": "180:230:220:150",
            "InTypes": {0: "HRP_IMAGE", 1: "HRP_INT", 2:"HRP_INT"},
            "OutTypes": {0: "HRP_IMAGE"},
            "Description": _("Morphological operation that connects objects on an image."),
            "TreeGroup": _("Morphological Operations")
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {
        "masksize":{"name": "Mask Size",
                    "type": HARPIA_COMBO,
                    "value": self.masksize,
                    "values": ["1x1", "3x3", "5x5", "7x7"]
                    }
        }

# ------------------------------------------------------------------------------
