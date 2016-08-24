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
        self.type = "81"
        self.masksize = "3"

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "operação de filtragem que calcula o Laplaciano de uma imagem,\
        realçando cantos e bordas de objetos."

    def generate(self, blockTemplate):
        blockTemplate.imagesIO = \
            'IplImage * block$$_img_i1 = NULL; //Laplace In \n' + \
            'IplImage * block$$_img_o1 = NULL; //Laplace Out \n' + \
            'IplImage * block$$_img_t = NULL;  //Laplace Temp \n' + \
            'int block$$_int_i2 = ' + str(self.masksize) + '; // Laplace Mask Size\n'

        blockTemplate.functionCall = '\nif(block$$_img_i1){\n' + \
                                     'block$$_int_i2 = (block$$_int_i2 > 31)? 31 : block$$_int_i2; // Laplace Mask Constraint\n' + \
                                     'block$$_int_i2 = (block$$_int_i2 % 2 == 0)? block$$_int_i2 + 1 : block$$_int_i2; // Only Odd\n' + \
                                     'block$$_img_o1 = cvCreateImage(cvSize(block$$' + \
                                     '_img_i1->width,block$$_img_i1->height), IPL_DEPTH_32F,block$$_img_i1->nChannels);\n' + \
                                     'cvLaplace(block$$_img_i1, block$$_img_o1 , block$$_int_i2 );}\n'

        blockTemplate.dealloc = 'cvReleaseImage(&block$$_img_o1);\n' + \
                                'cvReleaseImage(&block$$_img_i1);\n' + \
                                'cvReleaseImage(&block$$_img_t);\n'


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

