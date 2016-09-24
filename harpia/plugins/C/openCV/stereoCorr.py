#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin

class StereoCorr(OpenCVPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.maxDist = 60

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return 'Input1 is the left image and Input2 is the right image. Output is the depth image'

    # ----------------------------------------------------------------------
    def generate_vars(self):
        return \
            'IplImage * block$id$_img_i0 = NULL;\n' + \
            'IplImage * block$id$_img_i1 = NULL;\n' + \
            'IplImage * block$id$_img_o0 = NULL;\n' + \
            'IplImage * block$id$_img_ts0 = NULL;\n' + \
            'IplImage * block$id$_img_ts1 = NULL;\n'

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return \
            '\nif(block$id$_img_i0 && block$id$_img_i1)\n{\n' + \
            '	if(!block$id$_img_o0)\n' + \
            '		block$id$_img_o0 = cvCreateImage(cvGetSize(block$id$_img_i0), IPL_DEPTH_8U, 1);\n' + \
            '	if(!block$id$_img_ts0)\n' + \
            '		block$id$_img_ts0 = cvCreateImage(cvGetSize(block$id$_img_i0), IPL_DEPTH_8U, 1);\n' + \
            '	if(!block$id$_img_ts1)\n' + \
            '		block$id$_img_ts1 = cvCreateImage(cvGetSize(block$id$_img_i0), IPL_DEPTH_8U, 1);\n' + \
            '	cvCvtColor(block$id$_img_i0, block$id$_img_ts0, CV_BGR2GRAY);\n' + \
            '	cvCvtColor(block$id$_img_i1, block$id$_img_ts1, CV_BGR2GRAY);\n' + \
            '	cvFindStereoCorrespondence( block$id$_img_ts0, block$id$_img_ts1, CV_DISPARITY_BIRCHFIELD,' +\
            'block$id$_img_o0, $maxDist$, 15, 3, 6, 8, 15 );\n}\n'

    # ----------------------------------------------------------------------
    def generate_dealloc(self):
        return  'cvReleaseImage(&block$id$_img_o0);\n' + \
                'cvReleaseImage(&block$id$_img_i0);\n' + \
                'cvReleaseImage(&block$id$_img_i1);\n' + \
                'if(block$id$_img_ts0)\n\tcvReleaseImage(&block$id$_img_ts0);\n' + \
                'if(block$id$_img_ts1)\n\tcvReleaseImage(&block$id$_img_ts1);\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {'Label': _('Stereo Correspondence'),
            'Icon': 'images/stereoCorr.png',
            'Color': '10:10:20:150',
            'InTypes': {0: 'HRP_IMAGE', 1: "HRP_IMAGE"},
            'OutTypes': {0: 'HRP_IMAGE'},
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
