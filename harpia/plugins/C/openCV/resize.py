#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin

class Resize(OpenCVPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.id = -1
        self.type = self.__class__.__module__
        self.method = "CV_INTER_LINEAR"

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Resizes the input image to the dimensions of the input rectangle"

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return \
            'if(block$id$_img_i1){\n' + \
            'CvSize size$id$ = cvSize(block$id$_rect_i2.width,block$id$_rect_i2.height);\n' + \
            'block$id$_img_o1 = cvCreateImage(size$id$,block$id$_img_i1->depth,block$id$_img_i1->nChannels);\n' + \
            'cvResize(block$id$_img_i1, block$id$_img_o1, $method$);\n' + \
            '}\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            "Label": _("Resize Image"),
            "Icon": "images/resize.png",
            "Color": "20:80:10:150",
            "InTypes": {0: "HRP_IMAGE", 1: "HRP_RECT"},
            "OutTypes": {0: "HRP_IMAGE"},
            "Description": _("Resizes the input image to the dimensions of the input rectangle"),
            "TreeGroup": _("Experimental")
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {
        "method":{"name": "Method",
                    "type": HARPIA_COMBO,
                    "value": self.method,
                    "values": ["CV_INTER_NN", "CV_INTER_LINEAR" , "CV_INTER_AREA", "CV_INTER_CUBIC"]
                    }
        }

# ------------------------------------------------------------------------------
