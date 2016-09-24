#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin

class ComposeRGB(OpenCVPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "BLOCO Composição RGB"

    # ----------------------------------------------------------------------
    def generate_vars(self):
        return \
            'IplImage * block$id$_img_i0 = NULL;\n' + \
            'IplImage * block$id$_img_i1 = NULL;\n' + \
            'IplImage * block$id$_img_i2 = NULL;\n' + \
            'IplImage * block$id$_img_t0 = NULL;\n' + \
            'IplImage * block$id$_img_t1 = NULL;\n' + \
            'IplImage * block$id$_img_t2 = NULL;\n' + \
            'IplImage * block$id$_img_o0 = NULL;\n'

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return \
            '\nif(block$id$_img_i0){\n' + \
            'block$id$_img_o0 = cvCloneImage(block$id$_img_i0);\n' + \
            'CvSize size$id$ = cvSize(block$id$_img_i0->width,block$id$_img_i0->height);\n'+ \
            'block$id$_img_t0 = cvCreateImage(size$id$, block$id$_img_i0->depth, 1);\n'+\
            'block$id$_img_t1 = cvCreateImage(size$id$, block$id$_img_i0->depth, 1);\n'+\
            'block$id$_img_t2 = cvCreateImage(size$id$, block$id$_img_i0->depth, 1);\n'+\
            'cvSplit(block$id$_img_i0 ,block$id$_img_t0  ,NULL, NULL , NULL);\n' + \
            'cvSplit(block$id$_img_i1 ,NULL ,block$id$_img_t1, NULL, NULL);\n' + \
            'cvSplit(block$id$_img_i2 ,NULL ,NULL, block$id$_img_t2 , NULL);\n' + \
            'cvMerge(block$id$_img_t2 ,block$id$_img_t1 ,block$id$_img_t0 , NULL, block$id$_img_o0);}\n'

    # ----------------------------------------------------------------------
    def generate_dealloc(self):
        return 'cvReleaseImage(&block$id$_img_t0);\n' + \
               'cvReleaseImage(&block$id$_img_t1);\n' + \
               'cvReleaseImage(&block$id$_img_t2);\n' + \
               'cvReleaseImage(&block$id$_img_o0);\n' + \
               'cvReleaseImage(&block$id$_img_i0);\n' + \
               'cvReleaseImage(&block$id$_img_i1);\n' + \
               'cvReleaseImage(&block$id$_img_i2);\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
         "Label":_("Compose RGB"),
         "Icon":"images/composeRGB.png",
         "Color":"50:125:50:150",
         "InTypes":{0:"HRP_IMAGE",1:"HRP_IMAGE",2:"HRP_IMAGE"},
         "OutTypes":{0:"HRP_IMAGE"},
         "Description":_("Compose three color channels  (R, G and B)  into one color image."),
         "TreeGroup":_("Filters and Color Conversion")
         }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {}

# ------------------------------------------------------------------------------

