#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class PlotHistogram(OpenCVPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.channel = "All"

        # Appearance
        self.help = "Create a representation of the light " + \
            "intensity levels as an histogram."
        self.label = "Histogram"
        self.icon = "images/plotHistogram.png"
        self.color = "0:0:0:150"
        self.in_types = ["HRP_IMAGE"]
        self.out_types = ["HRP_IMAGE"]
        self.group = "Histograms"

        self.properties = {
            "channel": {
                "name": "Channels",
                "type": HARPIA_COMBO,
                "values": ["All", "Red", "Green", "Blue"]
            }
        }

        # -------------------C/OpenCv code------------------------------------
        self.vars = \
            'IplImage * block$id$_img_i0 = NULL;\n' + \
            'IplImage * block$id$_img_o0 = NULL;\n' + \
            'CvHistogram * block$id$_histogram;\n' + \
            'IplImage * block$id$_SourceCx[] = { NULL, NULL, NULL};\n' + \
            'IplImage * block$id$_HistCx[] = { NULL, NULL, NULL};\n' + \
            'int block$id$_histogram_size[] = { 255, 255, 255 };\n' + \
            'float * block$id$_hist_ranges[] = { NULL, NULL, NULL};\n' + \
            'float block$id$_hist_rang[2];\n' + \
            'float block$id$_histBin;\n' + \
            'float block$id$_histMaxVal;\n' + \
            'int block$id$_histV;\n' + \
            'int block$id$_plotHistChanIter;\n' + \
            'int block$id$_plotHistArrIter;\n'

        self.dealloc = \
            'if(block$id$_SourceCx[0]) cvReleaseImage' + \
            '(&block$id$_SourceCx[0]);\n' + \
            'if(block$id$_SourceCx[1]) cvReleaseImage' + \
            '(&block$id$_SourceCx[1]);\n' + \
            'if(block$id$_SourceCx[2]) cvReleaseImage' + \
            '(&block$id$_SourceCx[2]);\n' + \
            'if(block$id$_HistCx[0]) cvReleaseImage' + \
            '(&block$id$_HistCx[0]);\n' + \
            'if(block$id$_HistCx[1]) ' + \
            'cvReleaseImage(&block$id$_HistCx[1]);\n' + \
            'if(block$id$_HistCx[2]) ' + \
            'cvReleaseImage(&block$id$_HistCx[2]);\n' + \
            'if(block$id$_img_i0) cvReleaseImage(&block$id$_img_i0);\n' + \
            'if(block$id$_img_o0) cvReleaseImage(&block$id$_img_o0);\n' + \
            'cvReleaseHist(&block$id$_histogram);\n'

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        ChannelValue = '3'
        HistValue = '0'
        if self.channel == 'All':
            ChannelValue = '3'
            HistValue = '0'
        elif self.channel == 'Red':
            ChannelValue = '3'
            HistValue = '2'
        elif self.channel == 'Green':
            ChannelValue = '2'
            HistValue = '1'
        elif self.channel == 'Blue':
            ChannelValue = '1'
            HistValue = '0'
        return \
            '\nif(block$id$_img_i0 && block$id$_img_i0->nChannels == 3){\n' + \
            '  block$id$_img_o0 = cvCreateImage' + \
            '(cvSize(255,300), IPL_DEPTH_8U,3);\n' + \
            '  block$id$_SourceCx[0] = cvCreateImage(cvSize(block$id$' + \
            '_img_i0->width,block$id$_img_i0->height), IPL_DEPTH_8U, 1);\n' + \
            '  block$id$_SourceCx[1] = cvCreateImage(cvSize(block$id$' + \
            '_img_i0->width,block$id$_img_i0->height), IPL_DEPTH_8U, 1);\n' + \
            '  block$id$_SourceCx[2] = cvCreateImage(cvSize(block$id$' + \
            '_img_i0->width,block$id$_img_i0->height), IPL_DEPTH_8U, 1);\n' + \
            '  block$id$_HistCx[0] = cvCreateImage' + \
            '(cvSize(255,300), IPL_DEPTH_8U, 1);\n' + \
            '  block$id$_HistCx[1] = cvCreateImage' + \
            '(cvSize(255,300), IPL_DEPTH_8U, 1);\n' + \
            '  block$id$_HistCx[2] = cvCreateImage' + \
            '(cvSize(255,300), IPL_DEPTH_8U, 1);\n' + \
            '  cvSplit(block$id$_img_i0,block$id$_SourceCx[0],' + \
            '  block$id$_SourceCx[1],block$id$_SourceCx[2], NULL);\n' + \
            '  block$id$_hist_rang[0] = 0;\n' + \
            '  block$id$_hist_rang[1] = 255;\n' + \
            '  block$id$_hist_ranges[0] = block$id$_hist_rang;\n' + \
            '  block$id$_hist_ranges[1] = block$id$_hist_rang;\n' + \
            '  block$id$_hist_ranges[2] = block$id$_hist_rang;\n' + \
            '  block$id$_histogram = cvCreateHist' + \
            '( 1, block$id$_histogram_size,' + \
            ' CV_HIST_ARRAY, block$id$_hist_ranges, 1);\n' + \
            '  for(block$id$_plotHistChanIter =' + HistValue + ';' + \
            'block$id$_plotHistChanIter<' + ChannelValue + ';' \
            'block$id$_plotHistChanIter++)\n' + \
            '  {\n' + \
            '      cvCalcHist( &block$id$_SourceCx' + \
            '[block$id$_plotHistChanIter],' + \
            'block$id$_histogram, 0,NULL);\n' + \
            '      cvSetZero(block$id$_HistCx' + \
            '[block$id$_plotHistChanIter]);\n' + \
            '      cvGetMinMaxHistValue(block$id$_histogram,0, ' + \
            '&block$id$_histMaxVal, NULL,NULL);\n' + \
            '      for(block$id$_plotHistArrIter=0; ' + \
            'block$id$_plotHistArrIter<255;' + \
            'block$id$_plotHistArrIter++)\n' + \
            '      {\n' + \
            '          block$id$_histBin = ' + \
            'cvQueryHistValue_1D(block$id$_histogram,' + \
            'block$id$_plotHistArrIter);\n' + \
            '          block$id$_histV=(int)((block$id$_histBin/' + \
            'block$id$_histMaxVal)*300);\n' + \
            '          block$id$_histV=block$id$_HistCx' + \
            '[block$id$_plotHistChanIter]->height - 1 - block$id$_histV;\n' + \
            '          cvLine(block$id$_HistCx[block$id$_plotHist' + \
            'ChanIter], cvPoint(block$id$_plotHistArrIter' + \
            ',block$id$_histV), cvPoint(block$id$_plotHistArrIter,' + \
            'block$id$_HistCx[block$id$_plotHistChanIter]->height' \
            ' - 1),cvScalarAll(255),1, CV_AA,0 );' + \
            '      }\n' + \
            '  }\n' + \
            '  cvMerge(block$id$_HistCx[0],' + \
            'block$id$_HistCx[1],block$id$_HistCx[2],' + \
            ' NULL,block$id$_img_o0);\n' + \
            '}\n' + \
            'else\n' + \
            '{\n' + \
            '  block$id$_img_o0 = cvCreateImage' + \
            '(cvSize(255,300), IPL_DEPTH_8U,1);\n' + \
            '  block$id$_SourceCx[0] = cvCreateImage(cvSize(block$id$' + \
            '_img_i0->width,block$id$_img_i0->height), IPL_DEPTH_8U, 1);\n' + \
            '  block$id$_hist_rang[0] = 0;\n' + \
            '  block$id$_hist_rang[1] = 255;\n' + \
            '  block$id$_hist_ranges[0] = block$id$_hist_rang;\n' + \
            '  block$id$_histogram = cvCreateHist' + \
            '( 1, block$id$_histogram_size,' + \
            ' CV_HIST_ARRAY, block$id$_hist_ranges, 1);\n' + \
            '  cvCalcHist( &block$id$_SourceCx[0], ' + \
            'block$id$_histogram, 0,NULL);\n' + \
            '  cvSetZero(block$id$_img_o0);\n' + \
            '  cvGetMinMaxHistValue(block$id$_histogram,0, ' + \
            '&block$id$_histMaxVal, NULL,NULL);\n' + \
            '  for(block$id$_plotHistArrIter=0;block$id$_' + \
            'plotHistArrIter<255;block$id$_plotHistArrIter++)\n' + \
            '  {\n' + \
            '      block$id$_histBin = cvQueryHistValue_1D' + \
            '(block$id$_histogram, block$id$_plotHistArrIter);\n' + \
            '      block$id$_histV=(int)((block$id$_histBin/' + \
            'block$id$_histMaxVal)*300);\n' + \
            '      block$id$_histV=block$id$_img_o0->' + \
            'height - 1 - block$id$_histV;\n' + \
            '      cvLine(block$id$_img_o0, cvPoint(block$id$_' + \
            'plotHistArrIter ,block$id$_histV), cvPoint' + \
            '(block$id$_plotHistArrIter,block$id$_img_o0->height' \
            ' - 1),cvScalarAll(255),1, 0,0 );\n' + \
            '  }\n' + \
            '}\n'

# -----------------------------------------------------------------------------
