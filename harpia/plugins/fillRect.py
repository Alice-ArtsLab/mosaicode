#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class FillRect(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        self.id = -1
        self.type = "14"
        self.color = "#0000ffff0000"

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return  "Preenche o retângulo de uma cor."

    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):
        red = self.color[1:5]
        green = self.color[5:9]
        blue = self.color[9:13]

        red = int(red, 16) / 257
        green = int(green, 16) / 257
        blue = int(blue, 16) / 257

        blockTemplate.imagesIO = \
            'IplImage * block$$_img_i1 = NULL;\n' + \
            'CvRect block$$_rect_i2;\n' + \
            'IplImage * block$$_img_o1 = NULL;\n'
        blockTemplate.functionCall = \
            '\nif(block$$_img_i1)\n{\n' + \
            '\tblock$$_img_o1 = cvCloneImage(block$$_img_i1);\n' + \
            '\tcvSetImageROI(block$$_img_o1 , block$$_rect_i2);\n' + \
            '\tCvScalar color = cvScalar('+blue +','+ green +','+ red+',0);\n' + \
            '\tcvSet(block$$_img_o1,color,NULL);\n' + \
            '\tcvResetImageROI(block$$_img_o1);\n' + \
            '}\n'
        blockTemplate.dealloc = 'cvReleaseImage(&block$$_img_o1);\n' + \
                      'cvReleaseImage(&block$$_img_i1);\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
                "Label":_("Fill Rectangle"),
                "Icon":"images/fill.png",
                "Color":"50:100:200:150",
                "InTypes":{0:"HRP_IMAGE",1:"HRP_RECT"},
                "OutTypes":{0:"HRP_IMAGE"},
                "Description":_("Fill the input rectangle on the input image with the desired color."),
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
