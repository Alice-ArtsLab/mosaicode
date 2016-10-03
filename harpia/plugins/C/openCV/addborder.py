#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin

class AddBorder(OpenCVPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.border = 50
        self.color = "#0000ffff0000"
        self.border_type = "IPL_BORDER_CONSTANT"
 
    # --------------------------Help Text--------------------------------------------
    def get_help(self):#Função que chama a help
        return "Adiciona bordas na imagem"


    # --------------------------Help Text--------------------------------------------
    def generate_vars(self):
        return "IplImage * block$id$_img_i0 = NULL;\n" + \
                "int block$id$_int_i1 = $border$;\n"+ \
                "IplImage * block$id$_img_o0 = NULL;\n"

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
            'int border=$border$;\n' + \
            'CvSize size$id$ = cvSize(block$id$_img_i0->width + border * 2, block$id$_img_i0->height + border * 2);\n' + \
            'block$id$_img_o0 = cvCreateImage(size$id$, block$id$_img_i0->depth,block$id$_img_i0->nChannels);\n' + \
            'CvPoint point$id$ = cvPoint(border, border);\n' + \
            'CvScalar color = cvScalar('+ str(blue) +','+ str(green) +','+ str(red) + ',0);\n' + \
            'cvCopyMakeBorder(block$id$_img_i0, block$id$_img_o0, point$id$, $border_type$, color);\n' + \
            '}\n'

    # ------------------------------------------------------------------------------
    def get_description(self):
        return {"Label": "Add Border",
                "Icon": "images/and.png",
                "Color": "0:180:210:150",
                "InTypes": {0: "HRP_IMAGE", 1:"HRP_INT"},
                "OutTypes": {0: "HRP_IMAGE"},
                "TreeGroup": "Experimental"
                }

    # ------------------------------------------------------------------------------
    def get_properties(self):
        return {
                   "color":{"name": "Color",
                     "type": HARPIA_COLOR
                    },
                "border_type":{"name": "Type",
                    "type": HARPIA_COMBO,
                    "values": ["IPL_BORDER_CONSTANT",
                            "IPL_BORDER_REPLICATE",
                            "IPL_BORDER_REFLECT",
                            "IPL_BORDER_WRAP"]
                    },
                 "border":{
                 "name": "Border Size",
                 "type": HARPIA_INT
                 }
                }

# ------------------------------------------------------------------------------
