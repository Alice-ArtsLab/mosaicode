# -*- coding: utf-8 -*-
# [HARPIA PROJECT]
#
#
# S2i - Intelligent Industrial Systems
# DAS - Automation and Systems Department
# UFSC - Federal University of Santa Catarina
# Copyright: 2006 - 2007 Luis Carlos Dill Junges (lcdjunges@yahoo.com.br), Clovis Peruchi Scotti (scotti@ieee.org),
#                        Guilherme Augusto Rutzen (rutzen@das.ufsc.br), Mathias Erdtmann (erdtmann@gmail.com) and S2i (www.s2i.das.ufsc.br)
#            2007 - 2009 Clovis Peruchi Scotti (scotti@ieee.org), S2i (www.s2i.das.ufsc.br)
#
#
#    This program is free software: you can redistribute it and/or modify it
#    under the terms of the GNU General Public License version 3, as published
#    by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranties of
#    MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
#    PURPOSE.  See the GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    For further information, check the COPYING file distributed with this software.
#
# ----------------------------------------------------------------------

import gtk

from harpia.GladeWindow import GladeWindow
from harpia.s2icommonproperties import S2iCommonProperties, APP, DIR

# i18n
import os
from harpia.utils.XMLUtils import XMLParser
import gettext

_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)


# ----------------------------------------------------------------------

class Properties(GladeWindow, S2iCommonProperties):
    # ----------------------------------------------------------------------

    def __init__(self, PropertiesXML, S2iBlockProperties):

        self.m_sDataDir = os.environ['HARPIA_DATA_DIR']

        filename = self.m_sDataDir + 'glade/plotHistogram.ui'
        self.m_oPropertiesXML = PropertiesXML
        self.m_oS2iBlockProperties = S2iBlockProperties

        widget_list = [
            'Properties',
            'HISTImageType',
            'HISTLabelChannel',
            'HISTRadioR',
            'HISTRadioG',
            'HISTRadioB',
            'BackgroundColor',
            'BorderColor',
            'HelpView'
        ]

        handlers = [
            # 'on_HISTRadioR_pressed',
            # 'on_HISTRadioG_pressed',
            # 'on_HISTRadioB_pressed',
            'on_HISTImageType_changed',
            'on_cancel_clicked',
            'on_histogram_confirm_clicked',
            'on_BackColorButton_clicked',
            'on_BorderColorButton_clicked'
        ]

        top_window = 'Properties'

        GladeWindow.__init__(self, filename, top_window, widget_list, handlers)

        # load properties values
        self.block_properties = self.m_oPropertiesXML.getTag("properties").getTag("block").getChildTags("property")
        for Property in self.block_properties:

            if Property.name == "type":
                if Property.value == "allcolors":
                    self.widgets['HISTImageType'].set_active(int(0))
                if Property.value == "color":
                    self.widgets['HISTImageType'].set_active(int(1))
                self.on_HISTImageType_changed()

            if Property.name == "channel":
                if Property.value == "R":
                    self.widgets['HISTRadioR'].set_active(True);
                if Property.value == "G":
                    self.widgets['HISTRadioG'].set_active(True);
                if Property.value == "B":
                    self.widgets['HISTRadioB'].set_active(True);

        self.configure()


        # # load help text
        # t_oS2iHelp = XMLParser(self.m_sDataDir + "help/plotHistogram" + _("_en.help"))

        # t_oTextBuffer = gtk.TextBuffer()

        # t_oTextBuffer.set_text(unicode(str(t_oS2iHelp.getTag("help").getTag("content").getTagContent())))

        # self.widgets['HelpView'].set_buffer(t_oTextBuffer)

    #--------------------------Help Text---------------------------------------

    def getHelp(self):#adicionado help
        return "Representação dos níveis de intensidade luminosa de uma imagem na forma de um histograma."


    # ----------------------------------------------------------------------

    def __del__(self):

        pass

    # ----------------------------------------------------------------------

    def on_histogram_confirm_clicked(self, *args):

        for Property in self.block_properties:

            if Property.name == "type":
                Active = self.widgets['HISTImageType'].get_active()
                if int(Active) == 0:
                    Property.value = unicode("allcolors")
                if int(Active) == 1:
                    Property.value = unicode("color")

            if Property.name == "channel":
                if self.widgets['HISTRadioR'].get_active():
                    Property.value = unicode("R")
                if self.widgets['HISTRadioG'].get_active():
                    Property.value = unicode("G")
                if self.widgets['HISTRadioB'].get_active():
                    Property.value = unicode("B")

        self.m_oS2iBlockProperties.SetPropertiesXML(self.m_oPropertiesXML)

        self.m_oS2iBlockProperties.SetBorderColor(self.m_oBorderColor)

        self.m_oS2iBlockProperties.SetBackColor(self.m_oBackColor)

        self.widgets['Properties'].destroy()

    # ----------------------------------------------------------------------

    def on_HISTImageType_changed(self, *args):

        if self.widgets['HISTImageType'].get_active() == int(0):
            self.widgets['HISTLabelChannel'].set_sensitive(False)
            self.widgets['HISTRadioR'].set_sensitive(False)
            self.widgets['HISTRadioG'].set_sensitive(False)
            self.widgets['HISTRadioB'].set_sensitive(False)
        else:
            self.widgets['HISTLabelChannel'].set_sensitive(True)
            self.widgets['HISTRadioR'].set_sensitive(True)
            self.widgets['HISTRadioG'].set_sensitive(True)
            self.widgets['HISTRadioB'].set_sensitive(True)

            # ----------------------------------------------------------------------


# HistogramProperties = Properties()
# HistogramProperties.show( center=0 )

# ------------------------------------------------------------------------------
# Code generation
# ------------------------------------------------------------------------------
def generate(blockTemplate):
    flag = ''
    for propIter in blockTemplate.properties:
        if propIter[0] == 'type':
            if (propIter[1] == 'allcolors'):
                ChannelValue = '3'
                HistValue = '0'
                flag = 'allColors'
            elif (propIter[1] == 'color'):
                flag = 'oneColor'
        if ((propIter[0] == 'channel') & (flag == 'oneColor')):
            if (propIter[1] == 'R'):
                ChannelValue = '3'
                HistValue = '2'
            if (propIter[1] == 'G'):
                ChannelValue = '2'
                HistValue = '1'
            if (propIter[1] == 'B'):
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
                                 '	block$$_SourceCx[0] = cvCreateImage(cvSize(block' + blockTemplate.blockNumber + \
                                 '_img_i1->width,block$$_img_i1->height), IPL_DEPTH_8U, 1);\n' + \
                                 '	block$$_SourceCx[1] = cvCreateImage(cvSize(block' + blockTemplate.blockNumber + \
                                 '_img_i1->width,block$$_img_i1->height), IPL_DEPTH_8U, 1);\n' + \
                                 '	block$$_SourceCx[2] = cvCreateImage(cvSize(block' + blockTemplate.blockNumber + \
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
                                 '	block$$_SourceCx[0] = cvCreateImage(cvSize(block' + blockTemplate.blockNumber + \
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


# ------------------------------------------------------------------------------
# Block Setup
# ------------------------------------------------------------------------------
def getBlock():
    return {"Label": _("Histogram"),
            "Path": {"Python": "plotHistogram",
                     "Glade": "glade/plotHistogram.ui",
                     "Xml": "xml/plotHistogram.xml"},
            "Icon": "images/plotHistogram.png",
            "Color": "0:0:0:150",
            "InTypes": {0: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "Description": _("Create a representation of the light intensity levels as an histogram."),
            "TreeGroup": _("Histograms")
            }
