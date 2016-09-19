#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin

class Opening(OpenCVPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.id = -1
        self.type = self.__class__.__module__
        self.masksize = "3x3"

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
            return "operação morfológica que visa desconectar objetos em uma imagem ou suprimir ruídos."

    # ----------------------------------------------------------------------
    def generate_vars(self):
        return \
            'IplImage * block$id$_img_i1 = NULL;\n' + \
            'IplImage * block$id$_img_o1 = NULL;\n' + \
            'IplConvKernel * block$id$' + \
            '_arg_mask = cvCreateStructuringElementEx(' + self.masksize[0] + ' , ' + \
            self.masksize[2] + ', 1, 1,CV_SHAPE_RECT,NULL);\n'

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return \
            '\nif(block$id$_img_i1){\n' + \
            'IplImage * block$id$_auxImg;' + \
            'block$id$_img_o1 = cvCloneImage(block$id$_img_i1);\n' + \
            'block$id$_auxImg = cvCloneImage(block$id$_img_i1);\n' + \
            'cvMorphologyEx(block$id$_img_i1,block$id$_img_o1,NULL,' + \
            'block$id$_arg_mask, CV_MOP_OPEN, 1);\n}\n'

    # ----------------------------------------------------------------------
    def generate_dealloc(self):
        return 'cvReleaseImage(&block$id$_img_o1);\n' + \
               'cvReleaseStructuringElement(&block$id$_arg_mask);\n' + \
               'cvReleaseImage(&block$id$_img_i1);\n'

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
