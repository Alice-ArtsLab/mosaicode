#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin

class Subtraction(OpenCVPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Realiza a subtração de duas imagens."

    # ----------------------------------------------------------------------
    def generate_header(self):
        return self.get_adjust_images_size()

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return \
            'if(block$id$_img_i0 && block$id$_img_i1){\n' + \
            'block$id$_img_o0 = cvCloneImage(block$id$_img_i0);\n' + \
            'adjust_images_size(block$id$_img_i0, block$id$_img_i1, block$id$_img_o0);\n' + \
            'cvSub(block$id$_img_i0, block$id$_img_i1, block$id$_img_o0,0);\n' + \
            'cvResetImageROI(block$id$_img_o0);\n'+ \
            '}\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            "Label": _("Subtraction"),
            "Icon": "images/subtraction.png",
            "Color": "180:10:10:150",
            "InTypes": {0: "HRP_IMAGE", 1: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "Description": _("Subtract two images."),
            "TreeGroup": _("Arithmetic and logical operations")
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {}

# ------------------------------------------------------------------------------
