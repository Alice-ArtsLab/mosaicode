#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class DecomposeRGB(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        self.id = -1
        self.type = "08"

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "BLOCO Decomposição RGB"
    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):
        blockTemplate.imagesIO = \
                     'IplImage * block$$_img_i1 = NULL;\n' + \
                     'IplImage * block$$_img_t1 = NULL;\n' + \
                     'IplImage * block$$_img_t2 = NULL;\n' + \
                     'IplImage * block$$_img_t3 = NULL;\n' + \
                     'IplImage * block$$_img_o1 = NULL;\n' + \
                     'IplImage * block$$_img_o2 = NULL;\n' + \
                     'IplImage * block$$_img_o3 = NULL;\n'
        blockTemplate.functionCall = \
                           '\nif(block$$_img_i1){\n' + \
                           'block$$_img_o1 = cvCreateImage(cvSize(block$$_img_i1->width,block$$_img_i1->height), block$$_img_i1->depth, block$$_img_i1->nChannels);\n'+\
                          'block$$_img_o2 = cvCreateImage(cvSize(block$$_img_i1->width,block$$_img_i1->height), block$$_img_i1->depth, block$$_img_i1->nChannels);\n'+\
                          'block$$_img_o3 = cvCreateImage(cvSize(block$$_img_i1->width,block$$_img_i1->height), block$$_img_i1->depth, block$$_img_i1->nChannels);\n' + \
                          'block$$_img_t1 = cvCreateImage(cvSize(block$$_img_i1->width,block$$_img_i1->height), block$$_img_i1->depth, 1);\n' + \
                          'block$$_img_t2 = cvCreateImage(cvSize(block$$_img_i1->width,block$$_img_i1->height), block$$_img_i1->depth, 1);\n' +\
                          'block$$_img_t3 = cvCreateImage(cvSize(block$$_img_i1->width,block$$_img_i1->height), block$$_img_i1->depth, 1);\n' + \
                          'cvSplit(block$$_img_i1 ,block$$_img_t3 ,block$$_img_t2 ,block$$_img_t1 , NULL);\n' + \
                          'cvMerge(block$$_img_t1 ,block$$_img_t1 , block$$_img_t1 , NULL, block$$_img_o1);\n' + \
                          'cvMerge(block$$_img_t2 ,block$$_img_t2, block$$_img_t2, NULL, block$$_img_o2);\n' + \
                          'cvMerge(block$$_img_t3 ,block$$_img_t3, block$$_img_t3, NULL, block$$_img_o3);}\n'
        blockTemplate.dealloc = 'cvReleaseImage(&block$$_img_t1);\n' + \
                      'cvReleaseImage(&block$$_img_t2);\n' + \
                      'cvReleaseImage(&block$$_img_t3);\n' + \
                      'cvReleaseImage(&block$$_img_o1);\n' + \
                      'cvReleaseImage(&block$$_img_o2);\n' + \
                      'cvReleaseImage(&block$$_img_o3);\n' + \
                      'cvReleaseImage(&block$$_img_i1);\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
         "Label":_("Decompose RGB"),
         "Icon":"images/decomposeRGB.png",
         "Color":"50:125:50:150",
         "InTypes":{0:"HRP_IMAGE"},
         "OutTypes":{0:"HRP_IMAGE",1:"HRP_IMAGE",2:"HRP_IMAGE"},
         "Description":_("Decompose a color image in three color channels (R, G and B)."),
         "TreeGroup":_("Filters and Color Conversion")
         }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {}

# ------------------------------------------------------------------------------
