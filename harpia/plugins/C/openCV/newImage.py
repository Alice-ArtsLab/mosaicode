#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin

class NewImage(OpenCVPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.width = "640"
        self.height = "480"

    # ----------------------------------------------------------------------
    def get_help(self):
        return "Cria uma nova imagem."

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return \
            'CvSize size = cvSize($width$,$height$);\n' + \
            'block$id$_img_o0 = cvCreateImage(size,IPL_DEPTH_8U,3);\n' + \
            'cvSetZero(block$id$_img_o0);\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
         "Label":_("New Image"),
         "Icon":"images/acquisition.png",
         "Color":"50:100:200:150",
         "InTypes":"",
         "OutTypes":{0:"HRP_IMAGE"},
         "Description":_("Create a new image."),
         "TreeGroup":_("Image Source"),
         "IsSource":True
         }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {

        "width":{"name": "Width",
                    "type": HARPIA_INT,
                    "value": self.width,
                    "lower":0,
                    "upper":65535,
                    "step":1
                    },
        "height":{"name": "Height",
                    "type": HARPIA_INT,
                    "value": self.height,
                    "lower":0,
                    "upper":65535,
                    "step":1
                    }
        }

# ------------------------------------------------------------------------------
