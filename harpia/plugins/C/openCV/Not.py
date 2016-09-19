#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class Not(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)
        self.id = -1
        self.type = self.__class__.__module__

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Realiza a negação lógica de uma imagem. Corresponde à negativa da imagem."

    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):
        blockTemplate.imagesIO = "\n //NOT input and output \n"
        blockTemplate.imagesIO += \
            'IplImage * block$id$_img_i1 = NULL; // NOT input\n' + \
            'IplImage * block$id$_img_o1 = NULL; // NOT output\n'
        blockTemplate.imagesIO += "\n\n"

        blockTemplate.functionCall = "\n\n // NOT Execution Block\n"
        blockTemplate.functionCall += 'if(block$id$_img_i1){\n' + \
                                      'block$id$_img_o1 = cvCreateImage(cvSize(block$id$' + \
                                      '_img_i1->width,block$id$_img_i1->height),block$id$' + \
                                      '_img_i1->depth,block$id$_img_i1->nChannels);\n'
        blockTemplate.functionCall += 'cvNot(block$id$_img_i1, block$id$_img_o1);\n}\n'

        blockTemplate.dealloc = '// NOT dealloc block '
        blockTemplate.dealloc += 'cvReleaseImage(&block$id$_img_o1);\n'
        blockTemplate.dealloc += 'cvReleaseImage(&block$id$_img_i1);\n'
        blockTemplate.dealloc = '\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            "Label": _("Not"),
            "Icon": "images/not.png",
            "Color": "10:180:10:150",
            "InTypes": {0: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "Description": _("Negate the image. It is equivalent to the negative image."),
            "TreeGroup": _("Arithmetic and logical operations")
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {}

# ------------------------------------------------------------------------------
