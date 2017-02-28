#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the StereoCorr class.
"""
from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class StereoCorr(OpenCVPlugin):
    """
    This class contains methods related the StereoCorr class.
    """
    # -------------------------------------------------------------------------

    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.maxDist = 60

        # Appearance
        self.help = 'Input1 is the left image and Input2 " + \
            "is the right image. Output is the depth image.'
        self.label = "images/stereoCorr.png"
        self.color = "10:10:20:150"
        self.in_types = ["HRP_IMAGE", "HRP_IMAGE"]
        self.out_types = ["HRP_IMAGE"]
        self.group = "Feature Detection"

        self.properties = [{"name": "Max Distance",
                            "label": "maxDist",
                            "type": HARPIA_INT,
                            "lower": 0,
                            "upper": 655,
                            "step": 1
                            }
                           ]

        # -------------------C/OpenCv code------------------------------------
        self.vars = \
            'IplImage * block$id$_img_i0 = NULL;\n' + \
            'IplImage * block$id$_img_i1 = NULL;\n' + \
            'IplImage * block$id$_img_o0 = NULL;\n' + \
            'IplImage * block$id$_img_ts0 = NULL;\n' + \
            'IplImage * block$id$_img_ts1 = NULL;\n'

        self.function_call = \
            '\nif(block$id$_img_i0 && block$id$_img_i1)\n{\n' + \
            '   if(!block$id$_img_o0)\n' + \
            '       block$id$_img_o0 = cvCreateImage' + \
            '(cvGetSize(block$id$_img_i0), IPL_DEPTH_8U, 1);\n' + \
            '   if(!block$id$_img_ts0)\n' + \
            '       block$id$_img_ts0 = cvCreateImage' + \
            '(cvGetSize(block$id$_img_i0), IPL_DEPTH_8U, 1);\n' + \
            '   if(!block$id$_img_ts1)\n' + \
            '       block$id$_img_ts1 = cvCreateImage' + \
            '(cvGetSize(block$id$_img_i0), IPL_DEPTH_8U, 1);\n' + \
            '   cvCvtColor(block$id$_img_i0, ' + \
            'block$id$_img_ts0, CV_BGR2GRAY);\n' + \
            '   cvCvtColor(block$id$_img_i1, ' + \
            'block$id$_img_ts1, CV_BGR2GRAY);\n' + \
            '   cvFindStereoCorrespondence' + \
            '(block$id$_img_ts0, block$id$_img_ts1, ' + \
            'CV_DISPARITY_BIRCHFIELD,' +\
            'block$id$_img_o0, $maxDist$, 15, 3, 6, 8, 15 );\n}\n'

        self.dealloc = \
            'cvReleaseImage(&block$id$_img_o0);\n' + \
            'cvReleaseImage(&block$id$_img_i0);\n' + \
            'cvReleaseImage(&block$id$_img_i1);\n' + \
            'if(block$id$_img_ts0)\n\tcvReleaseImage' + \
            '(&block$id$_img_ts0);\n' + \
            'if(block$id$_img_ts1)\n\tcvReleaseImage(&block$id$_img_ts1);\n'

# -----------------------------------------------------------------------------
