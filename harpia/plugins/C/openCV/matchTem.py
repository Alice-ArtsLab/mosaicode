#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin

class MatchTem(OpenCVPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.method = 'CV_TM_SQDIFF'
        self.scaleFactor = 6

        self.help = "Operação de filtragem destinada a suavizar uma imagem."
        
        self.description = {
            "Label": "Match Template",
            "Icon": "images/matchTem.png",
            "Color": "180:180:10:150",
            "InTypes": {0: "HRP_IMAGE", 1: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "TreeGroup": "Feature Detection"
        }

        self.properties = {
            "scaleFactor":{ 
                "name": "Scale Factor",
                "type": HARPIA_INT,
                "lower":0,
                "upper":99,
                "step":1
            },
            "method":{
                "name": "Method",
                "type": HARPIA_COMBO,
                "values": ["CV_TM_CCOEFF_NORMED", "CV_TM_CCOEFF",
                                "CV_TM_CCORR_NORMED", "CV_TM_CCORR",
                                "CV_TM_SQDIFF_NORMED", "CV_TM_SQDIFF"
                ]
            }
        }

        #------------------------------C/OpenCv code---------------------------
        self.vars = \
            'IplImage * block$id$_img_i0 = NULL;\n' + \
            'IplImage * block$id$_img_i1 = NULL;\n' + \
            'IplImage * block$id$_img_t0 = NULL;\n' + \
            'IplImage * block$id$_img_o0 = NULL;\n'

        self.function_call =  \
            'if(block$id$_img_i0 && block$id$_img_i1){\n' + \
            '\tdouble width$id$ = block$id$_img_i0->width - block$id$_img_i1->width +1;\n' + \
            '\tdouble height$id$ = block$id$_img_i0->height - block$id$_img_i1->height +1;\n'+ \
            '\tCvSize size$id$ = cvSize(width$id$,height$id$);\n' + \
            '\tblock$id$_img_t0 = cvCreateImage(size$id$,32,1);\n' + \
            '\tblock$id$_img_o0 = cvCreateImage(size$id$,8,1);\n' + \
            '\tcvMatchTemplate(block$id$_img_i0 , block$id$_img_i1, block$id$_img_t0, $method$);\n' + \
            '\tcvConvertScale(block$id$_img_t0, block$id$_img_o0, ' + str(
            10 ** -(int(float(self.scaleFactor)))) + ',0);\n' + \
            '}\n'

        self.dealloc = \
            'cvReleaseImage(&block$id$_img_o0);\n' + \
            'cvReleaseImage(&block$id$_img_t0);\n' + \
            'cvReleaseImage(&block$id$_img_i1);\n' + \
            'cvReleaseImage(&block$id$_img_i0);\n' 

    # ----------------------------------------------------------------------
    def get_help(self):
        return self.help

    # ----------------------------------------------------------------------
    def get_description(self):
        return self.description

    # ----------------------------------------------------------------------
    def get_properties(self):
        return self.properties

    # ----------------------------------------------------------------------
    def generate_vars(self):
        return self.vars

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return self.function_call

    # ----------------------------------------------------------------------
    def generate_dealloc(self):
        return self.dealloc

# ------------------------------------------------------------------------------

