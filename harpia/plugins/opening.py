#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class Opening(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        self.id = -1
        self.type = "102"
        self.masksize = "3x3"

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
            return "operação morfológica que visa desconectar objetos em uma imagem ou suprimir ruídos."

    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):
        blockTemplate.imagesIO = \
            'IplImage * block$$_img_i1 = NULL;\n' + \
            'IplImage * block$$_img_o1 = NULL;\n'
        blockTemplate.imagesIO += 'IplConvKernel * block$$' + \
                                          '_arg_mask = cvCreateStructuringElementEx(' + self.masksize[0] + ' , ' + \
                                          self.masksize[2] + ', 1, 1,CV_SHAPE_RECT,NULL);\n'
        blockTemplate.functionCall = '\nif(block$$_img_i1){\n' + \
                                     'IplImage * block$$_auxImg;' + \
                                     'block$$_img_o1 = cvCreateImage(cvSize(block$$' + \
                                     '_img_i1->width, block$$_img_i1->height), block$$' + \
                                     '_img_i1->depth ,block$$_img_i1->nChannels);\n' + \
                                     '\nblock$$_auxImg = cvCreateImage(cvSize(block$$' + \
                                     '_img_i1->width, block$$_img_i1->height), block$$' + \
                                     '_img_i1->depth ,block$$_img_i1->nChannels);\n' + \
                                     'cvMorphologyEx(block$$_img_i1,block$$_img_o1,NULL,' + \
                                     'block$$_arg_mask, CV_MOP_OPEN, 1);\n}\n'
        blockTemplate.dealloc = 'cvReleaseImage(&block$$_img_o1);\n' + \
                                'cvReleaseStructuringElement(&block$$_arg_mask);\n' + \
                                'cvReleaseImage(&block$$_img_i1);\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            "Label": _("Opening"),
            "Icon": "images/opening.png",
            "Color": "180:230:220:150",
            "InTypes": {0: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "Description": _("Morphological operation that disconnects objects and reduces noise."),
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

# -----------------------------------------------------------------------------
