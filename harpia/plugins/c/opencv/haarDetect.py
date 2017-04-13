#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the HaarDetect class.
"""
from harpia.GUI.fieldtypes import *
from harpia.plugins.c.opencv.opencvplugin import OpenCVPlugin


class HaarDetect(OpenCVPlugin):
    """
    This class contains methods related the HaarDetect class.
    """
    # -------------------------------------------------------------------------

    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.cascade_name = "/usr/share/harpia/images/" + \
            "haarcascade_frontalface_alt2.xml"
        self.min_neighbors = 2

        # Appearance
        self.help = 'Haar (face) Detector finds regions on the input ' + \
            'image according to the given haar-classifier. \n' + \
            'First Output is the center of the first detected feature, ' + \
            'second is a rectangle around the first ' + \
            'detected feature and the third is the input image with ' + \
            'the detected features tagged by a red circle.\n' + \
            'The last output is the number of detected faces.'
        self.label = "Haar Detector"
        self.color = "50:220:40:150"
        self.in_types = ["HRP_IMAGE"]
        self.out_types = ["HRP_POINT", "HRP_RECT", "HRP_IMAGE", "HRP_DOUBLE"]
        self.group = "Feature Detection"

        self.properties = [{"name": "File Name",
                            "label": "cascade_name",
                            "type": HARPIA_SAVE_FILE
                            },
                           {"name": "Min neighbors",
                            "label": "min_neighbors",
                            "type": HARPIA_INT,
                            "lower": 1,
                            "upper": 99,
                            "step": 1
                            },
                           ]

        # ------------------------------C/OpenCv code--------------------------
        self.codes[1] = \
            'IplImage * block$id$_img_i0 = NULL;\n' + \
            'CvPoint block$id$_point_o0 = cvPoint(0,0);\n' + \
            'CvRect block$id$_rect_o1 = cvRect( 0, 0, 1, 1);\n' + \
            'IplImage * block$id$_img_o2 = NULL;\n' + \
            'double block$id$_double_o3 = 0.0;\n' + \
            'static CvMemStorage* block$id$_storage = 0;\n' + \
            'static CvHaarClassifierCascade* block$id$_cascade = 0;\n' + \
            'const char* block$id$_cascade_name = "$cascade_name$";\n'

        self.codes[2] = \
            '\nif(block$id$_img_i0){\n' + \
            '  double scale = 1.3;\n' + \
            '  block$id$_cascade = (CvHaarClassifierCascade*)' + \
            'cvLoad( block$id$_cascade_name, 0, 0, 0 );\n' + \
            '  IplImage* gray = cvCreateImage( cvSize' + \
            '(block$id$_img_i0->width,block$id$_img_i0->height), 8, 1 );\n' + \
            '  IplImage* small_img = cvCreateImage' + \
            '( cvSize( cvRound (block$id$_img_i0->width/scale), cvRound ' + \
            '(block$id$_img_i0->height/scale)),8, 1 );\n' + \
            '  cvCvtColor( block$id$_img_i0, gray, CV_BGR2GRAY );\n' + \
            '  cvResize( gray, small_img, CV_INTER_LINEAR );\n' + \
            '  cvEqualizeHist( small_img, small_img );\n' + \
            '  if(!block$id$_img_o2)\n' + \
            '  block$id$_img_o2 = cvCloneImage(block$id$_img_i0);\n' + \
            '  cvCopy(block$id$_img_i0,block$id$_img_o2,0);\n' + \
            '  block$id$_storage = cvCreateMemStorage(0);\n' + \
            '  cvClearMemStorage( block$id$_storage );\n' + \
            '  block$id$_rect_o1 = cvRect( 0, 0, 1, 1);\n' + \
            '  CvSeq* faces = cvHaarDetectObjects(small_img, ' + \
            'block$id$_cascade, block$id$_storage,' + \
            '1.1,$min_neighbors$, 0/*CV_HAAR_DO_CANNY_PRUNING*/,' + \
            'cvSize(30, 30) );\n' + \
            '  block$id$_double_o3 = faces->total;\n' + \
            '  if(faces)\n' + \
            '  {\n' + \
            '      int i;\n' + \
            '      for( i = 0; i < (faces ? faces->total : 0); i++ )\n' + \
            '      {\n' + \
            '      CvRect* r = (CvRect*)cvGetSeqElem( faces, i );\n' + \
            '          if(r)\n' + \
            '          {\n' + \
            '              CvPoint center;\n' + \
            '              int radius;\n' + \
            '              center.x = cvRound((r->x + ' + \
            'r->width*0.5)*scale);\n' + \
            '              center.y = cvRound((r->y + ' + \
            'r->height*0.5)*scale);\n' + \
            '              radius = cvRound((r->width + ' + \
            'r->height)*0.25*scale);\n' + \
            '              cvCircle( block$id$_img_o2, center, ' + \
            'radius, cvScalarAll(0), 3, 8, 0 );\n' + \
            '              if(i == 0)\n' + \
            '              {\n' + \
            '                  block$id$_point_o0 = center;\n' + \
            '                  block$id$_rect_o1.x = (r->x)*scale;\n' + \
            '                  block$id$_rect_o1.y = (r->y)*scale;\n' + \
            '                  block$id$_rect_o1.width ' + \
            '= (r->width)*scale;\n' + \
            '                  block$id$_rect_o1.height' + \
            ' = (r->height)*scale;\n' + \
            '              }\n' + \
            '          }\n' + \
            '      }\n' + \
            '  }\n' + \
            '  cvReleaseImage( &gray );\n' + \
            '  cvReleaseImage( &small_img );\n' + \
            '}\n'

        self.codes[3] = \
            'cvReleaseImage(&block$id$_img_o2);\n' + \
            'cvReleaseImage(&block$id$_img_i0);\n' + \
            'cvReleaseMemStorage(&block$id$_storage);\n'

# -----------------------------------------------------------------------------
