#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin

class Fill(OpenCVPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.color = "#0000ffff0000"

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Preenche toda a imagem de uma cor."

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        red = self.color[1:5]
        green = self.color[5:9]
        blue = self.color[9:13]

        red = int(red, 16) / 257
        green = int(green, 16) / 257
        blue = int(blue, 16) / 257
        return \
            'if(block$id$_img_i0){\n' + \
            'block$id$_img_o0 = cvCloneImage(block$id$_img_i0);\n' + \
            'CvScalar color = cvScalar('+ str(blue) +','+ str(green) +','+ str(red) + ',0);\n' + \
            'cvSet(block$id$_img_o0, color, NULL);\n' + \
            '}\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
        "Label":_("Fill image"),
        "Icon":"images/fill.png",
        "Color":"50:100:200:150",
        "InTypes":{0:"HRP_IMAGE"},
        "OutTypes":{0:"HRP_IMAGE"},
        "Description":_("Fill an image with the desired color."),
        "TreeGroup":_("General")
      }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {
            "color":{"name": "Color",
                     "type": HARPIA_COLOR,
                     "value": self.color
                    }
        }

# ------------------------------------------------------------------------------
