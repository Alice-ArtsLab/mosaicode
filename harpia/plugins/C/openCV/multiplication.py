#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class Multiplication(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)
        self.id = -1
        self.type = self.__class__.__module__

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "realiza a multiplicação de duas imagens."
    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):
        import opencvcommon
        blockTemplate.header += opencvcommon.adjust_images_size()

        blockTemplate.imagesIO = \
            'IplImage * block$id$_img_i1 = NULL;\n' + \
            'IplImage * block$id$_img_i2 = NULL;\n' + \
            'IplImage * block$id$_img_o1 = NULL;\n'
        blockTemplate.functionCall = '\nif(block$id$_img_i1){\n' + \
            'block$id$_img_o1 = cvCreateImage(cvSize(block$id$' + \
            '_img_i1->width,block$id$_img_i1->height),block$id$' + \
            '_img_i1->depth,block$id$_img_i1->nChannels);\n' + \
            'adjust_images_size(block$id$_img_i1, block$id$_img_i2, block$id$_img_o1);\n' + \
            'cvMul(block$id$_img_i1, block$id$_img_i2, block$id$' + \
            '_img_o1,1);\n cvResetImageROI(block$id$_img_o1);}\n'
        blockTemplate.dealloc = 'cvReleaseImage(&block$id$_img_o1);\n' + \
                                'cvReleaseImage(&block$id$_img_i1);\n' + \
                                'cvReleaseImage(&block$id$_img_i2);\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            "Label": _("Multiplication"),
            "Icon": "images/multiplication.png",
            "Color": "180:10:10:150",
            "InTypes": {0: "HRP_IMAGE", 1: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "Description": _("Multiplies two images"),
            "TreeGroup": _("Arithmetic and logical operations")
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {}

# ------------------------------------------------------------------------------

