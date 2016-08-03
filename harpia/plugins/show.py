#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class Show(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        self.id = -1
        self.type = "02"
        self.title = "My Image"

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Mostra uma imagem da cadeia de processamento de imagens."

    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):
        blockTemplate.imagesIO = \
            'IplImage * block$$_img_i1 = NULL;\n' + \
            'IplImage * block$$_img_o1 = NULL;\n'
        blockTemplate.functionCall = '\nif(block$$_img_i1){\n' + \
                         'block$$_img_o1 = cvCloneImage(block$$_img_i1);\n' + \
                         'cvNamedWindow("' + self.title + '",CV_WINDOW_AUTOSIZE );\n' + \
                         'cvShowImage("' + self.title + '",block$$_img_i1);\n' + \
                         '\n}\n'
        blockTemplate.dealloc = 'cvReleaseImage(&block$$_img_o1);\n' + \
                                'cvReleaseImage(&block$$_img_i1);\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            "Label": _("Show Image"),
            "Icon": "images/show.png",
            "Color": "50:100:200:150",
            "InTypes": {0: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "Description": _("Shows the input image on a new window."),
            "TreeGroup": _("General")
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
