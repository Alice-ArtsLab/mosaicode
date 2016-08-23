#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class PlotHistogram(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        self.id = -1
        self.type = "03"
        self.channel = "All"

    # ----------------------------------------------------------------------
    def get_help(self):
        return "Create a representation of the light intensity levels as an histogram."
    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):
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

        blockTemplate.imagesIO = \
            'IplImage * block$$_img_i1 = NULL;\n' + \
            'IplImage * block$$_img_o1 = NULL;\n' + \
            'CvHistogram * block$$_histogram;\n' + \
            'IplImage * block$$_SourceCx[] = { NULL, NULL, NULL};\n' + \
            'IplImage * block$$_HistCx[] = { NULL, NULL, NULL};\n' + \
            'int block$$_histogram_size[] = { 255, 255, 255 };\n' + \
            'float * block$$_hist_ranges[] = { NULL, NULL, NULL};\n' + \
            'float block$$_hist_rang[2];\n' + \
            'float block$$_histBin;\n' + \
            'float block$$_histMaxVal;\n' + \
            'int block$$_histV;\n' + \
            'int block$$_plotHistChanIter;\n' + \
            'int block$$_plotHistArrIter;\n'
        blockTemplate.functionCall = '\nif(block$$_img_i1 && block$$_img_i1->nChannels == 3){\n' + \
             '	block$$_img_o1 = cvCreateImage(cvSize(255,300), IPL_DEPTH_8U,3);\n' + \
             '	block$$_SourceCx[0] = cvCreateImage(cvSize(block$$'+ \
             '_img_i1->width,block$$_img_i1->height), IPL_DEPTH_8U, 1);\n' + \
             '	block$$_SourceCx[1] = cvCreateImage(cvSize(block$$'+ \
             '_img_i1->width,block$$_img_i1->height), IPL_DEPTH_8U, 1);\n' + \
             '	block$$_SourceCx[2] = cvCreateImage(cvSize(block$$'+ \
             '_img_i1->width,block$$_img_i1->height), IPL_DEPTH_8U, 1);\n' + \
             '	block$$_HistCx[0] = cvCreateImage(cvSize(255,300), IPL_DEPTH_8U, 1);\n' + \
             '	block$$_HistCx[1] = cvCreateImage(cvSize(255,300), IPL_DEPTH_8U, 1);\n' + \
             '	block$$_HistCx[2] = cvCreateImage(cvSize(255,300), IPL_DEPTH_8U, 1);\n' + \
             '	cvSplit(block$$_img_i1,block$$_SourceCx[0],' + \
             '	block$$_SourceCx[1],block$$_SourceCx[2], NULL);\n' + \
             '	block$$_hist_rang[0] = 0;\n' + \
             '	block$$_hist_rang[1] = 255;\n' + \
             '	block$$_hist_ranges[0] = block$$_hist_rang;\n' + \
             '	block$$_hist_ranges[1] = block$$_hist_rang;\n' + \
             '	block$$_hist_ranges[2] = block$$_hist_rang;\n' + \
             '	block$$_histogram = cvCreateHist( 1, block$$_histogram_size,' + \
             ' CV_HIST_ARRAY, block$$_hist_ranges, 1);\n' + \
             '	for(block$$_plotHistChanIter =' + HistValue + ';block$$_plotHistChanIter<' + ChannelValue + ';' \
             'block$$_plotHistChanIter++)\n' + \
             '	{\n' + \
             '		cvCalcHist( &block$$_SourceCx[block$$_plotHistChanIter],' + \
             'block$$_histogram, 0,NULL);\n' + \
             '		cvSetZero(block$$_HistCx[block$$_plotHistChanIter]);\n' + \
             '		cvGetMinMaxHistValue(block$$_histogram,0, &block$$_histMaxVal, NULL,NULL);\n' + \
             '		for(block$$_plotHistArrIter=0;block$$_plotHistArrIter<255;' + \
             'block$$_plotHistArrIter++)\n' + \
             '		{\n' + \
             '			block$$_histBin = cvQueryHistValue_1D(block$$_histogram,' + \
             'block$$_plotHistArrIter);\n' + \
             '			block$$_histV=(int)((block$$_histBin/block$$_histMaxVal)*300);\n' + \
             '			block$$_histV=block$$_HistCx[block$$_plotHistChanIter]->height - 1 - block$$_histV;\n' + \
             '			cvLine(block$$_HistCx[block$$_plotHistChanIter], cvPoint(block$$_plotHistArrIter' + \
             ',block$$_histV), cvPoint(block$$_plotHistArrIter,block$$_HistCx[block$$_plotHistChanIter]->height' \
             ' - 1),cvScalarAll(255),1, CV_AA,0 );' + \
             '		}\n' + \
             '	}\n' + \
             '	cvMerge(block$$_HistCx[0],' + \
             'block$$_HistCx[1],block$$_HistCx[2],' + \
             ' NULL,block$$_img_o1);\n' + \
             '}\n' + \
             'else\n' + \
             '{\n' + \
             '	block$$_img_o1 = cvCreateImage(cvSize(255,300), IPL_DEPTH_8U,1);\n' + \
             '	block$$_SourceCx[0] = cvCreateImage(cvSize(block$$'+ \
             '_img_i1->width,block$$_img_i1->height), IPL_DEPTH_8U, 1);\n' + \
             '	block$$_hist_rang[0] = 0;\n' + \
             '	block$$_hist_rang[1] = 255;\n' + \
             '	block$$_hist_ranges[0] = block$$_hist_rang;\n' + \
             '	block$$_histogram = cvCreateHist( 1, block$$_histogram_size,' + \
             ' CV_HIST_ARRAY, block$$_hist_ranges, 1);\n' + \
             '	cvCalcHist( &block$$_SourceCx[0], block$$_histogram, 0,NULL);\n' + \
             '	cvSetZero(block$$_img_o1);\n' + \
             '	cvGetMinMaxHistValue(block$$_histogram,0, &block$$_histMaxVal, NULL,NULL);\n' + \
             '	for(block$$_plotHistArrIter=0;block$$_plotHistArrIter<255;block$$_plotHistArrIter++)\n' + \
             '	{\n' + \
             '		block$$_histBin = cvQueryHistValue_1D(block$$_histogram, block$$_plotHistArrIter);\n' + \
             '		block$$_histV=(int)((block$$_histBin/block$$_histMaxVal)*300);\n' + \
             '		block$$_histV=block$$_img_o1->height - 1 - block$$_histV;\n' + \
             '		cvLine(block$$_img_o1, cvPoint(block$$_plotHistArrIter ,block$$_histV), cvPoint(block$$_plotHistArrIter,block$$_img_o1->height' \
             ' - 1),cvScalarAll(255),1, 0,0 );\n' + \
             '	}\n' + \
             '}\n'
        blockTemplate.dealloc = 'if(block$$_SourceCx[0]) cvReleaseImage(&block$$_SourceCx[0]);\n' + \
            'if(block$$_SourceCx[1]) cvReleaseImage(&block$$_SourceCx[1]);\n' + \
            'if(block$$_SourceCx[2]) cvReleaseImage(&block$$_SourceCx[2]);\n' + \
            'if(block$$_HistCx[0]) cvReleaseImage(&block$$_HistCx[0]);\n' + \
            'if(block$$_HistCx[1]) cvReleaseImage(&block$$_HistCx[1]);\n' + \
            'if(block$$_HistCx[2]) cvReleaseImage(&block$$_HistCx[2]);\n' + \
            'if(block$$_img_i1) cvReleaseImage(&block$$_img_i1);\n' + \
            'if(block$$_img_o1) cvReleaseImage(&block$$_img_o1);\n' + \
            'cvReleaseHist(&block$$_histogram);\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            "Label": _("Histogram"),
            "Icon": "images/plotHistogram.png",
            "Color": "0:0:0:150",
            "InTypes": {0: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "Description": _("Create a representation of the light intensity levels as an histogram."),
            "TreeGroup": _("Histograms")
            }
    # ----------------------------------------------------------------------
    def get_properties(self):
        return {

        "channel":{"name": "Channels",
                    "type": HARPIA_COMBO,
                    "value": self.channel,
                    "values": ["All", "Red", "Green", "Blue"]
                    }

        }

# ------------------------------------------------------------------------------
