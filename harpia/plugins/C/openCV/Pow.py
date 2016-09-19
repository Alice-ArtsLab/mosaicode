#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin

class Pow(OpenCVPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.id = -1
        self.type = self.__class__.__module__
        self.exponent = 1

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Eleva cada ponto de uma imagem a um valor fixo de potência."

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return \
            '\nif(block$id$_img_i1){\n' + \
            'block$id$_img_o1 = cvCloneImage(block$id$_img_i1);\n' + \
            'cvPow(block$id$_img_i1, block$id$_img_o1, $exponent$);\n' + \
            '}\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            "Label": _("Pow"),
            "Icon": "images/pow.png",
            "Color": "230:230:60:150",
            "InTypes": {0: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "Description": _("Power each pixel value to a fixed value."),
            "TreeGroup": _("Math Functions")
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {"exponent":{"name": "Exponent",
                            "type": HARPIA_INT,
                            "value": self.exponent,
                            "lower":1,
                            "upper":10,
                            "step":1
                            }
                }

# ------------------------------------------------------------------------------

