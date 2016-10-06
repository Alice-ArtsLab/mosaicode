#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin

class FillRect(OpenCVPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.color = "#0000ffff0000"

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return  "Preenche o retângulo de uma cor."

    # ----------------------------------------------------------------------
    def generate_vars(self):
        return \
            'IplImage * block$id$_img_i0 = NULL;\n' + \
            'CvRect block$id$_rect_i1;\n' + \
            'IplImage * block$id$_img_o0 = NULL;\n'

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        red = self.color[1:5]
        green = self.color[5:9]
        blue = self.color[9:13]

        red = int(red, 16) / 257
        green = int(green, 16) / 257
        blue = int(blue, 16) / 257
        return \
            '\nif(block$id$_img_i0)\n{\n' + \
            '\tblock$id$_img_o0 = cvCloneImage(block$id$_img_i0);\n' + \
            '\tcvSetImageROI(block$id$_img_o0 , block$id$_rect_i1);\n' + \
            '\tCvScalar color = cvScalar('+ str(blue) +','+ str(green) +','+ str(red)+',0);\n' + \
            '\tcvSet(block$id$_img_o0,color,NULL);\n' + \
            '\tcvResetImageROI(block$id$_img_o0);\n' + \
            '}\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Label":"Fill Rectangle",
                "Icon":"images/fill.png",
                "Color":"50:100:200:150",
                "InTypes":{0:"HRP_IMAGE",1:"HRP_RECT"},
                "OutTypes":{0:"HRP_IMAGE"},
                "TreeGroup":"Basic Shapes"
         }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {
            "color":{"name": "Color",
                     "type": HARPIA_COLOR
                    }
        }
# ------------------------------------------------------------------------------
