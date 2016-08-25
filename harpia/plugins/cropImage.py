#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class CropImage(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)
        self.id = -1
        self.type = "802"

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Corta a Imagem de acordo com o Retangulo\n de entrada."

    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):
        blockTemplate.imagesIO = \
            'IplImage * block$$_img_i1 = NULL;\n' + \
            'IplImage * block$$_img_o1 = NULL;\n' + \
            'CvRect  block$$_rect_i2;\n'
        blockTemplate.functionCall = '\nif(block$$_img_i1){\n' + \
                                     '	block$$_rect_i2.x = MAX(0,block$$_rect_i2.x);//Check whether point is negative\n' + \
                                     '	block$$_rect_i2.y = MAX(0,block$$_rect_i2.y);\n' + \
                                     '	block$$_rect_i2.x = MIN(block$$_img_i1->width-1,block$$_rect_i2.x);//Check whether point is out of the image\n' + \
                                     '	block$$_rect_i2.y = MIN(block$$_img_i1->height-1,block$$_rect_i2.y);\n' + \
                                     '	block$$_rect_i2.width = MIN(block$$_img_i1->width-block$$_rect_i2.x,block$$_rect_i2.width);//Check whether rect reaches out of the image\n' + \
                                     '	block$$_rect_i2.height = MIN(block$$_img_i1->height-block$$_rect_i2.y,block$$_rect_i2.height);\n' + \
                                     '	block$$_img_o1 = cvCreateImage(cvSize(block$$_rect_i2.width,block$$_rect_i2.height),' + \
                                     ' block$$_img_i1->depth,block$$_img_i1->nChannels);\n' + \
                                     '	cvSetImageROI(block$$_img_i1,block$$_rect_i2);\n' + \
                                     '	cvCopyImage(block$$_img_i1,block$$_img_o1);\n' + \
                                     '}\n'
        blockTemplate.dealloc = 'cvReleaseImage(&block$$_img_o1);\n' + \
                                'cvReleaseImage(&block$$_img_i1);\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            'Label': _('Crop Image'),
            'Icon': 'images/cropImage.png',
            'Color': '50:50:200:150',
            'InTypes': {0: 'HRP_IMAGE', 1: 'HRP_RECT'},
            'OutTypes': {0: 'HRP_IMAGE'},
            'Description': _('Crops the input image according to input Rectangle'),
            'TreeGroup': _('Experimental')
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {}

# ------------------------------------------------------------------------------

