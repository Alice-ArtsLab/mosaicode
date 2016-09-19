#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class Save(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)
        self.id = -1
        self.type = self.__class__.__module__
        self.filename = ""

# ------------------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
                "Label": "Save Image",
                "Icon": "images/save.png",
                "Color": "50:100:200:150",
                "InTypes": {0: "HRP_IMAGE"},
                "OutTypes": {0: "HRP_IMAGE"},
                "Description": "Save image on a file indicated by the user.",
                "TreeGroup": "General"
                }

# ------------------------------------------------------------------------------
    def generate(self, blockTemplate):
        blockTemplate.imagesIO = \
            'IplImage * block$id$_img_i1 = NULL;\n' + \
            'IplImage * block$id$_img_o1 = NULL;\n'
        blockTemplate.functionCall = \
            'block$id$_img_o1 = cvCloneImage(block$id$_img_i1);\n' + \
            '\nif(block$id$_img_i1)\n' + \
            'cvSaveImage("$filename$" ,block$id$_img_i1);\n'
        blockTemplate.dealloc = 'cvReleaseImage(&block$id$_img_o1);\n' + \
                                'cvReleaseImage(&block$id$_img_i1);\n'

# ------------------------------------------------------------------------------
    def get_properties(self):
        return {"filename":{"name": "File Name",
                            "type": HARPIA_SAVE_FILE,
                            "value": self.filename}
                }

# ------------------------------------------------------------------------------
    def get_help(self):
        return "Salva uma imagem em uma mídia indicada pelo usuário.\
        Atualmente a imagem é salva como PNG por padrão." 

# ------------------------------------------------------------------------------
