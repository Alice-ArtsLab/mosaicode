#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin

class CropImage(OpenCVPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.x0 = 0
        self.y0 = 0
        self.width = 640
        self.height = 480

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Corta a Imagem de acordo com o Retangulo\n de entrada."

    # ----------------------------------------------------------------------
    def generate_vars(self):
        return \
            'IplImage * block$id$_img_i0 = NULL;\n' + \
            'IplImage * block$id$_img_o0 = NULL;\n' + \
            'CvRect  block$id$_rect_i1 = cvRect($x0$, $y0$, $width$, $height$);\n'

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return \
            '\nif(block$id$_img_i0){\n' + \
            '	block$id$_rect_i1.x = MAX(0,block$id$_rect_i1.x);//Check whether point is negative\n' + \
            '	block$id$_rect_i1.y = MAX(0,block$id$_rect_i1.y);\n' + \
            '	block$id$_rect_i1.x = MIN(block$id$_img_i0->width-1,block$id$_rect_i1.x);//Check whether point is out of the image\n' + \
            '	block$id$_rect_i1.y = MIN(block$id$_img_i0->height-1,block$id$_rect_i1.y);\n' + \
            '	block$id$_rect_i1.width = MIN(block$id$_img_i0->width-block$id$_rect_i1.x,block$id$_rect_i1.width);//Check whether rect reaches out of the image\n' + \
            '	block$id$_rect_i1.height = MIN(block$id$_img_i0->height-block$id$_rect_i1.y,block$id$_rect_i1.height);\n' + \
            '	block$id$_img_o0 = cvCreateImage(cvSize(block$id$_rect_i1.width,block$id$_rect_i1.height),' + \
            ' block$id$_img_i0->depth,block$id$_img_i0->nChannels);\n' + \
            '	cvSetImageROI(block$id$_img_i0,block$id$_rect_i1);\n' + \
            '	cvCopyImage(block$id$_img_i0,block$id$_img_o0);\n' + \
            '}\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {'Label': 'Crop Image',
            'Icon': 'images/cropImage.png',
            'Color': '50:50:200:150',
            'InTypes': {0: 'HRP_IMAGE', 1: 'HRP_RECT'},
            'OutTypes': {0: 'HRP_IMAGE'},
            'TreeGroup': 'Experimental'
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {"x0":{"name": "X",
                            "type": HARPIA_INT,
                            "lower":1,
                            "upper":65535,
                            "step":1
                            },
                "y0":{"name": "Y",
                            "type": HARPIA_INT,
                            "lower":1,
                            "upper":65535,
                            "step":1
                            },
                "width":{"name": "Width",
                            "type": HARPIA_INT,
                            "lower":1,
                            "upper":65535,
                            "step":1
                            },
                "height":{"name": "Height",
                            "type": HARPIA_INT,
                            "lower":1,
                            "upper":65535,
                            "step":1
                            }
                }

# ------------------------------------------------------------------------------

