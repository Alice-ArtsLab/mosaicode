#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class Dilate(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)
        self.id = -1
        self.type = self.__class__.__module__
        self.masksize = "3x3"
        self.iterations = 1

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "operação morfológica que provoca dilatação nos objetos de uma imagem, aumentando suas dimensões."

    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):
        blockTemplate.imagesIO = \
            'IplImage * block$$_img_i1 = NULL;\n' + \
            'IplImage * block$$_img_o1 = NULL;\n' + \
            'int block$$_arg_iterations = $iterations$;\n' + \
            'IplConvKernel * block$$_arg_mask = cvCreateStructuringElementEx(' + \
                    str(self.masksize[0]) + ' , ' + \
                    str(self.masksize[2]) + ', 1, 1,CV_SHAPE_RECT,NULL);\n'

        blockTemplate.functionCall = '''
if(block$$_img_i1){
    block$$_img_o1 = cvCreateImage(cvSize(block$$_img_i1->width,
            block$$_img_i1->height),
            block$$_img_i1->depth,
            block$$_img_i1->nChannels);
    cvDilate(block$$_img_i1,
            block$$_img_o1,
            block$$_arg_mask,
            block$$_arg_iterations);
}
'''

        blockTemplate.dealloc = 'cvReleaseImage(&block$$_img_o1);\n' + \
                                'cvReleaseImage(&block$$_img_i1);\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            "Label": _("Dilate"),
            "Icon": "images/dilate.png",
            "Color": "180:230:220:150",
            "InTypes": {0: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "Description": _("Morphological operation that dilates the objects of the image, enlarging their size."),
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
