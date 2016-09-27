#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin

class Show(OpenCVPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.title = "My Image"

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Mostra uma imagem da cadeia de processamento de imagens."

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return \
            '\nif(block$id$_img_i0){\n' + \
            'block$id$_img_o0 = cvCloneImage(block$id$_img_i0);\n' + \
            'cvNamedWindow("$title$",CV_WINDOW_AUTOSIZE );\n' + \
            'cvShowImage("$title$",block$id$_img_i0);\n' + \
            '\n}\n'

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Label": "Show Image",
            "Icon": "images/show.png",
            "Color": "50:100:200:150",
            "InTypes": {0: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "TreeGroup": "General"
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {
        "title":{"name": "Window Title",
                    "type": HARPIA_STRING,
                    "value": self.title
                    }
        }

# ------------------------------------------------------------------------------
