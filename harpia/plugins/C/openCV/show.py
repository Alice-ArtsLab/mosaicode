#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin

class Show(OpenCVPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.title = "My Image"
        self.window_type = "Image Size"

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Mostra uma imagem da cadeia de processamento de imagens."

    # ----------------------------------------------------------------------
    def generate_vars(self):
        code = OpenCVPlugin.generate_vars(self)
        if self.window_type == "Window Size":
            code += 'cvNamedWindow("$title$",CV_WINDOW_NORMAL);\n'
        elif self.window_type == "Resizable Window":
            code += 'cvNamedWindow("$title$",CV_WINDOW_NORMAL);\n'
        else:
            code += 'cvNamedWindow("$title$",CV_WINDOW_AUTOSIZE);\n'
        return  code

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        code = '\nif(block$id$_img_i0){\n' + \
            'block$id$_img_o0 = cvCloneImage(block$id$_img_i0);\n' + \
            'cvShowImage("$title$",block$id$_img_i0);\n'
        if self.window_type == "Window Size":
            code += 'cvSetWindowProperty("$title$", CV_WND_PROP_FULLSCREEN, CV_WINDOW_FULLSCREEN);\n'
        code += '\n}\n'
        return code

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
                    "type": HARPIA_STRING
                    },
        "window_type":{"name":"Window Type",
                "type":HARPIA_COMBO,
                "values": ["Window Size", "Image Size", "Resizable Window"]
                    }
        }

# ------------------------------------------------------------------------------
