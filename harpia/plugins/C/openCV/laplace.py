#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class Laplace(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)
        self.id = -1
        self.type = self.__class__.__module__
        self.masksize = "3"

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "operação de filtragem que calcula o Laplaciano de uma imagem,\
        realçando cantos e bordas de objetos."

    def generate(self, blockTemplate):
        self.masksize = int(self.masksize)
        blockTemplate.imagesIO = \
            'IplImage * block$id$_img_i1 = NULL; //Laplace In \n' + \
            'IplImage * block$id$_img_o1 = NULL; //Laplace Out \n' + \
            'IplImage * block$id$_img_t = NULL;  //Laplace Temp \n' + \
            'int block$id$_int_i2 = $masksize$; // Laplace Mask Size\n'

        blockTemplate.functionCall = '\nif(block$id$_img_i1){\n' + \
            'block$id$_int_i2 = (block$id$_int_i2 > 31)? 31 : block$id$_int_i2; // Laplace Mask Constraint\n' + \
            'block$id$_int_i2 = (block$id$_int_i2 % 2 == 0)? block$id$_int_i2 + 1 : block$id$_int_i2; // Only Odd\n' + \
            'block$id$_img_o1 = cvCreateImage(cvSize(block$id$' + \
            '_img_i1->width,block$id$_img_i1->height), IPL_DEPTH_32F,block$id$_img_i1->nChannels);\n' + \
            'cvLaplace(block$id$_img_i1, block$id$_img_o1 , block$id$_int_i2 );}\n'

        blockTemplate.dealloc = 'cvReleaseImage(&block$id$_img_o1);\n' + \
                                'cvReleaseImage(&block$id$_img_i1);\n' + \
                                'cvReleaseImage(&block$id$_img_t);\n'


    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            "Label": _("Laplace"),
            "Icon": "images/laplace.png",
            "Color": "250:180:80:150",
            "InTypes": {0: "HRP_IMAGE", 1: "HRP_INT"},
            "OutTypes": {0: "HRP_IMAGE"},
            "Description": _("Filtering operation that uses the Laplacian mask to enhance edges on the image."),
            "TreeGroup": _("Gradients, Edges and Corners")
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {
        "masksize":{"name": "Mask Size",
                    "type": HARPIA_COMBO,
                    "value": self.masksize,
                    "values": ["1", "3", "5", "7", "9", "11", "13"]
                    }
        }

# ------------------------------------------------------------------------------

