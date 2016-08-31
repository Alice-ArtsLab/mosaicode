#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class And(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)
        self.id = -1
        self.type = self.__class__.__module__

    # --------------------------Help Text--------------------------------------------
    def get_help(self):#Função que chama a help
        return "Permite a operação lógica 'E' entre as duas entradas. Para esse bloco há duas possibilidades.\
        Primeira: Executa a operação entre duas imagens ponto a ponto.\
        Segunda: Executa a operação entre um valor constante e cada ponto da imagem."

    # ------------------------------------------------------------------------------
    def generate(self, blockTemplate):
        import opencvcommon
        blockTemplate.header = opencvcommon.adjust_images_size()

        blockTemplate.imagesIO = \
            'IplImage * block$$_img_i1 = NULL;\n' + \
            'IplImage * block$$_img_i2 = NULL;\n' + \
            'IplImage * block$$_img_o1 = NULL;\n'
        blockTemplate.functionCall = '\nif(block$$_img_i1){\n' + \
                                     'block$$_img_o1 = cvCreateImage(cvSize(block$$' + \
                                     '_img_i1->width,block$$_img_i1->height),block$$' + \
                                     '_img_i1->depth,block$$_img_i1->nChannels);\n' + \
                                     'adjust_images_size(block$$_img_i1, block$$_img_i2, block$$_img_o1);\n' + \
                                     'cvAnd(block$$_img_i1, block$$_img_i2, block$$' + \
                                     '_img_o1,0);\ncvResetImageROI(block$$_img_o1);}\n'
        blockTemplate.dealloc = 'cvReleaseImage(&block$$_img_o1);\n' + \
                                'cvReleaseImage(&block$$_img_i1);\n' + \
                                'cvReleaseImage(&block$$_img_i2);\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ------------------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
                "Label": "And",
                "Icon": "images/and.png",
                "Color": "10:180:10:150",
                "InTypes": {0: "HRP_IMAGE", 1: "HRP_IMAGE"},
                "OutTypes": {0: "HRP_IMAGE"},
                "Description": "Logical AND operation between two images.",
                "TreeGroup": "Arithmetic and logical operations"
                }

    # ------------------------------------------------------------------------------
    def get_properties(self):
        return {}

# ------------------------------------------------------------------------------
