#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from plugins.plugin import Plugin
from constants import *

Plugin = Save()

class Save(Plugin):

    def __init__(self):
        self.titulo = "Meu Titulo"
        self.autor = ""
        self.editora = ""
        self.qtde_paginas = 0
        self.ano = 2016
        self.preco = 49.99
        pass

    # ------------------------------------------------------------------------------
    # Code generation
    # ------------------------------------------------------------------------------
    def generate(blockTemplate):
        for propIter in blockTemplate.properties:
            if propIter[0] == 'filename':
                saveFilename = os.path.expanduser(propIter[1])
        blockTemplate.imagesIO = \
            'IplImage * block$$_img_i1 = NULL;\n' + \
            'IplImage * block$$_img_o1 = NULL;\n'
        blockTemplate.functionCall = \
            'block$$_img_o1 = cvCloneImage(block$$_img_i1);\n' + \
            '\nif(block$$_img_i1)\n' + \
            'cvSaveImage("' + saveFilename + '" ,block$$_img_i1);\n'
        blockTemplate.dealloc = 'cvReleaseImage(&block$$_img_o1);\n' + \
                                'cvReleaseImage(&block$$_img_i1);\n'


    # ------------------------------------------------------------------------------
    # Block Setup
    # ------------------------------------------------------------------------------
    def getBlock():
        return {"Id":"01",
                "Label": "Save Image",
                "Path": {"Python": "save",
                         "Glade": "glade/save.ui",
                         "Xml": "xml/save.xml"},
                "Icon": "images/save.png",
                "Color": "50:100:200:150",
                "InTypes": {0: "HRP_IMAGE"},
                "OutTypes": {0: "HRP_IMAGE"},
                "Description": "Save image on a file indicated by the user.",
                "TreeGroup": "General"
                }
