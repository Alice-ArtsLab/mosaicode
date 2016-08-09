#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class Rotate(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        self.id = -1
        self.type = "607"
        self.isCenter = True
        self.isScalling = True
        self.isFilling = True
        self.xC = 20
        self.yC = 20
        self.angle = 0

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Rotates input image the input angle degrees."

    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):
        blockTemplate.header += "#define PI 3.1415926535898\n"
        blockTemplate.header += "double rads(double degs){\n"
        blockTemplate.header += "   return (PI/180 * degs);\n"
        blockTemplate.header += "}\n\n"


        blockTemplate.imagesIO = 'IplImage * block$$_img_i1 = NULL;\n' + \
                                 'double block$$_double_i2 = ' + str(self.angle) + ';\n' + \
                                 'IplImage * block$$_img_o1 = NULL;\n'
        blockTemplate.imagesIO += '\n\n'


        blockTemplate.functionCall = '\n	if(block$$_img_i1)\n	{\n' + \
                                     '		double scale;\n	int H;\n	int W;\n' + \
                                     '		W = block$$_img_i1->width;\n' + \
                                     '		H = block$$_img_i1->height;\n' + \
                                     '		block$$_img_o1 = cvCreateImage(cvSize(W,H),block$$_img_i1->depth,block$$_img_i1->nChannels);\n' + \
                                     '		CvMat* mat = cvCreateMat(2,3,CV_32FC1);\n'
        if self.isCenter == "true":
            blockTemplate.functionCall += '		CvPoint2D32f center = cvPoint2D32f(W/2, H/2);\n'
        else:
            blockTemplate.functionCall += '		CvPoint2D32f center = cvPoint2D32f(' + str(int(float(self.xC))) + ',' + str(
                int(float(self.yC))) + ');\n'

        if self.isScalling == "true":
            blockTemplate.functionCall += '		scale = H/(fabs(H*sin(rads(90-abs(block$$_double_i2)))) + fabs(W*sin(rads(abs(block$$_double_i2)))));\n' + \
                                          '		cv2DRotationMatrix(center,block$$_double_i2,scale,mat);\n'
        else:
            blockTemplate.functionCall += '		cv2DRotationMatrix(center,block$$_double_i2,1.0,mat);\n'

        if self.isFilling == "true":
            blockTemplate.functionCall += '		cvWarpAffine(block$$_img_i1,block$$_img_o1,mat,CV_WARP_FILL_OUTLIERS,cvScalarAll(0));\n'
        else:
            blockTemplate.functionCall += '		cvWarpAffine(block$$_img_i1,block$$_img_o1,mat,0,cvScalarAll(0));\n'

        blockTemplate.functionCall += '	}\n'
        blockTemplate.dealloc = 'cvReleaseImage(&block$$_img_o1);\n' + \
                                'cvReleaseImage(&block$$_img_i1);\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            "Label": _("Rotate Image"),
            "Icon": "images/rotate.png",
            "Color": "90:5:10:150",
            "InTypes": {0: "HRP_IMAGE", 1: "HRP_DOUBLE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "Description": _("Rotates input image the input angle degrees. (More options inside)"),
            "TreeGroup": _("Experimental")
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {
        "isCenter":{"name": "Use Image Center",
                            "type": HARPIA_CHECK,
                            "value": self.isCenter
                            },
        "isScalling":{"name": "Resize Image To Fit In",
                            "type": HARPIA_CHECK,
                            "value": self.isScalling
                            },
        "isFilling":{"name": "Fill Leftovers",
                            "type": HARPIA_CHECK,
                            "value": self.isFilling
                            },
        "xC":{"name": "Point X",
                    "type": HARPIA_INT,
                    "value": self.xC,
                    "lower":0,
                    "upper":65535,
                    "step":1
                    },
        "yC":{"name": "Point Y",
                    "type": HARPIA_INT,
                    "value": self.yC,
                    "lower":0,
                    "upper":65535,
                    "step":1
                    },
        "angle":{"name": "Angle",
                    "type": HARPIA_FLOAT,
                    "value": self.angle,
                    "lower":0,
                    "upper":360,
                    "step":1
                    }
        }

# ------------------------------------------------------------------------------

