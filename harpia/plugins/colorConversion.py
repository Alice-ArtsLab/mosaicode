#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class ColorConversion(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)
        self.id = -1
        self.type = "06"
        self.conversion_type = 'RGB -> GRAY'

    # ----------------------------------------------------------------------
    def get_help(self):
        return "Realiza a conversão de cores entre diferentes padrões de imagens coloridas e tons de cinza."
    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):
        channels = '3'
        if self.conversion_type == 'RGB -> GRAY':
            code = 'CV_RGB2GRAY'
            channels = '1';
        elif self.conversion_type == 'RGB -> YCrCb':
            code = 'CV_RGB2YCrCb'
        elif self.conversion_type == 'YCrCb -> RGB':
            code = 'CV_YCrCb2RGB'
        elif self.conversion_type == 'RGB -> HSV':
            code = 'CV_RGB2HSV'
        elif self.conversion_type == 'HSV -> RGB':
            code = 'CV_HSV2RGB'
        elif self.conversion_type == 'RGB -> HLS':
            code = 'CV_RGB2HLS'
        elif self.conversion_type == 'HLS -> RGB':
            code = 'CV_HLS2RGB'
        elif self.conversion_type == 'RGB -> CIE.XYZ':
            code = 'CV_RGB2XYZ'
        elif self.conversion_type == 'CIE.XYZ -> RGB':
            code = 'CV_XYZ2RGB'
        elif self.conversion_type == 'RGB -> CIE.LAB':
            code = 'CV_RGB2Lab'
        elif self.conversion_type == 'CIE.LAB -> RGB':
            code = 'CV_Lab2RGB'
        elif self.conversion_type == 'RGB -> CIE.LUV':
            code = 'CV_RGB2Luv'
        elif self.conversion_type == 'CIE.LUV -> RGB':
            code = 'CV_Luv2RGB'

        blockTemplate.imagesIO = \
            'IplImage * block$$_img_i1 = NULL;\n' + \
            'IplImage * block$$_img_o1 = NULL;\n' + \
            'IplImage * block$$_img_t = NULL;\n'

        blockTemplate.functionCall = '\nif(block$$_img_i1){\n' + \
                   'block$$_img_o1 = cvCreateImage(cvSize(block$$_img_i1->width,block$$_img_i1->height), block$$_img_i1->depth,block$$_img_i1->nChannels);\n' + \
                   'block$$_img_t = cvCreateImage(cvSize(block$$_img_i1->width,block$$_img_i1->height), block$$_img_i1->depth,' + channels + ');\n' + \
                   'cvCvtColor(block$$_img_i1, block$$_img_t ,' + code + ' );}\n' + \
                   'if ( ' + code + ' == ' + "CV_RGB2GRAY" + ')\n' + \
                   '{    cvMerge(block$$_img_t ,block$$_img_t ,block$$_img_t ,NULL ,block$$_img_o1);\n }\n' + \
                   'else\n' + '{ block$$_img_o1 = cvCloneImage(block$$_img_t);\n}'
 
        blockTemplate.dealloc = 'cvReleaseImage(&block$$_img_t);\n' + \
                                'cvReleaseImage(&block$$_img_i1);\n' + \
                                'cvReleaseImage(&block$$_img_o1);\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            "Label": _("Color Conversion"),
            "Icon": "images/colorConversion.png",
            "Color": "50:125:50:150",
            "InTypes": {0: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "Description": _("Convert colors between different standards of graylevel/color images."),
            "TreeGroup": _("Filters and Color Conversion")
            }
    # ----------------------------------------------------------------------
    def get_properties(self):
        return {

        "conversion_type":{"name": "Conversion Type",
                    "type": HARPIA_COMBO,
                    "value": self.conversion_type,
                    "values": ["RGB -> GRAY",
                                "RGB -> YCrCb",
                                "YCrCb -> RGB",
                                "RGB -> HSV",
                                "HSV -> RGB",
                                "RGB -> HLS",
                                "HLS -> RGB",
                                "RGB -> CIE.XYZ",
                                "CIE.XYZ -> RGB",
                                "RGB -> CIE.LAB",
                                "CIE.LAB -> RGB",
                                "RGB -> CIE.LUV",
                                "CIE.LUV -> RGB"]
                    }
        }

# ------------------------------------------------------------------------------
