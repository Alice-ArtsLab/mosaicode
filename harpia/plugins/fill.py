#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class Fill(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)
        self.id = -1
        self.type = self.__class__.__module__
        self.color = "#0000ffff0000"

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Preenche toda a imagem de uma cor."

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
            'IplImage * block$$_img_o1 = NULL;\n'
        blockTemplate.functionCall = \
            '\nif(block$$_img_i1){\n' + \
            'block$$_img_o1 = cvCloneImage(block$$_img_i1);\n' + \
            '\nCvScalar color = cvScalar('+ str(blue) +','+ str(green) +','+ str(red) + ',0);\n' + \
            '\ncvSet(block$$_img_o1,color,NULL);}\n'
        blockTemplate.dealloc = 'cvReleaseImage(&block$$_img_o1);\n' + \
          'cvReleaseImage(&block$$_img_i1);\n'

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
