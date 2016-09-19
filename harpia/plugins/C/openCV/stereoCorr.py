#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class StereoCorr(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)
        self.id = -1
        self.type = self.__class__.__module__
        self.maxDist = 60

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return 'Input1 is the left image and Input2 is the right image. Output is the depth image'

    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):
        blockTemplate.imagesIO = \
            'IplImage * block$id$_img_i1 = NULL;\n' + \
            'IplImage * block$id$_img_i2 = NULL;\n' + \
            'IplImage * block$id$_img_o1 = NULL;\n' + \
            'IplImage * block$id$_img_ts1 = NULL;\n' + \
            'IplImage * block$id$_img_ts2 = NULL;\n'
        blockTemplate.functionCall = '\nif(block$id$_img_i1 && block$id$_img_i2)\n{\n' + \
            '	if(!block$id$_img_o1)\n' + \
            '		block$id$_img_o1 = cvCreateImage(cvGetSize(block$id$_img_i1), IPL_DEPTH_8U, 1);\n' + \
            '	if(!block$id$_img_ts1)\n' + \
            '		block$id$_img_ts1 = cvCreateImage(cvGetSize(block$id$_img_i1), IPL_DEPTH_8U, 1);\n' + \
            '	if(!block$id$_img_ts2)\n' + \
            '		block$id$_img_ts2 = cvCreateImage(cvGetSize(block$id$_img_i1), IPL_DEPTH_8U, 1);\n' + \
            '	cvCvtColor(block$id$_img_i1, block$id$_img_ts1, CV_BGR2GRAY);\n' + \
            '	cvCvtColor(block$id$_img_i2, block$id$_img_ts2, CV_BGR2GRAY);\n' + \
            '	cvFindStereoCorrespondence( block$id$_img_ts1, block$id$_img_ts2, CV_DISPARITY_BIRCHFIELD,' +\
            'block$id$_img_o1, $maxDist$, 15, 3, 6, 8, 15 );\n}\n'

        blockTemplate.dealloc = 'cvReleaseImage(&block$id$_img_o1);\n' + \
            'cvReleaseImage(&block$id$_img_i1);\n' + \
            'cvReleaseImage(&block$id$_img_i2);\n' + \
            'if(block$id$_img_ts1)\n\tcvReleaseImage(&block$id$_img_ts1);\n' + \
            'if(block$id$_img_ts2)\n\tcvReleaseImage(&block$id$_img_ts2);\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            'Label': _('Stereo Correspondence'),
            'Icon': 'images/stereoCorr.png',
            'Color': '10:10:20:150',
            'InTypes': {0: 'HRP_IMAGE', 1: "HRP_IMAGE"},
            'OutTypes': {0: 'HRP_IMAGE'},
            'Description': _('Input1 is the left image and Input2 is the right image. Output is the depth image'),
            'TreeGroup': _('Feature Detection')
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {
        "maxDist":{"name": "Max Distance",
                    "type": HARPIA_INT,
                    "value": self.maxDist,
                    "lower":0,
                    "upper":655,
                    "step":1
                    }
        }

# ------------------------------------------------------------------------------
