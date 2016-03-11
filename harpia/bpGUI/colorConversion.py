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
import gettext
from harpia.utils.XMLUtils import XMLParser

_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)


# ----------------------------------------------------------------------

class Properties(GladeWindow, S2iCommonProperties):
    # ----------------------------------------------------------------------

    def __init__(self, PropertiesXML, S2iBlockProperties):

        self.m_sDataDir = os.environ['HARPIA_DATA_DIR']

        filename = self.m_sDataDir + 'glade/colorConversion.ui'
        self.m_oPropertiesXML = PropertiesXML
        self.m_oS2iBlockProperties = S2iBlockProperties

        widget_list = [
            'Properties',
            'COLOConversionType',
            'BackgroundColor',
            'BorderColor',
            'HelpView'
        ]

        handlers = [
            'on_BackColorButton_clicked',
            'on_BorderColorButton_clicked',
            'on_cancel_clicked',
            'on_colorConversion_confirm_clicked'
        ]

        top_window = 'Properties'

        GladeWindow.__init__(self, filename, top_window, widget_list, handlers)

        self.block_properties = self.m_oPropertiesXML.getTag("properties").getTag("block").getChildTags("property")
        #load properties values
        for Property in self.block_properties:

            name = Property.getAttr("name")
            value = Property.getAttr("value")

            if name == "type":
                if value == "RGB -> GRAY":
                    self.widgets['COLOConversionType'].set_active(int(0))
                if value == "RGB -> YCrCb":
                    self.widgets['COLOConversionType'].set_active(int(1))
                if value == "YCrCb -> RGB":
                    self.widgets['COLOConversionType'].set_active(int(2))
                if value == "RGB -> HSV":
                    self.widgets['COLOConversionType'].set_active(int(3))
                if value == "HSV -> RGB":
                    self.widgets['COLOConversionType'].set_active(int(4))
                if value == "RGB -> HLS":
                    self.widgets['COLOConversionType'].set_active(int(5))
                if value == "HLS -> RGB":
                    self.widgets['COLOConversionType'].set_active(int(6))
                if value == "RGB -> CIE.XYZ":
                    self.widgets['COLOConversionType'].set_active(int(7))
                if value == "CIE.XYZ -> RGB":
                    self.widgets['COLOConversionType'].set_active(int(8))
                if value == "RGB -> CIE.LAB":
                    self.widgets['COLOConversionType'].set_active(int(9))
                if value == "CIE.LAB -> RGB":
                    self.widgets['COLOConversionType'].set_active(int(10))
                if value == "RGB -> CIE.LUV":
                    self.widgets['COLOConversionType'].set_active(int(11))
                if value == "CIE.LUV -> RGB":
                    self.widgets['COLOConversionType'].set_active(int(12))

        self.configure()

        # load help text
        # t_oS2iHelp = XMLParser(self.m_sDataDir + "help/colorConversion" + _("_en.help"))

        # t_oTextBuffer = gtk.TextBuffer()

        # t_oTextBuffer.set_text(unicode(str(t_oS2iHelp.getTag("help").getTag("content").getTagContent())))

        # self.widgets['HelpView'].set_buffer(t_oTextBuffer)
    #-----------------------------------------------------------------
    def getHelp(self):
        return "Realiza a conversão de cores entre diferentes padrões de imagens coloridas e tons de cinza."

    # ----------------------------------------------------------------------

    def __del__(self):

        pass

    # ----------------------------------------------------------------------

    def on_colorConversion_confirm_clicked(self, *args):

        for Property in self.block_properties:

            name = Property.getAttr("name")

            if name == "type":
                Active = self.widgets['COLOConversionType'].get_active()
                if int(Active) == 0:
                    Property.setAttr("value", unicode("RGB -> GRAY"))
                if int(Active) == 1:
                    Property.setAttr("value", unicode("RGB -> YCrCb"))
                if int(Active) == 2:
                    Property.setAttr("value", unicode("YCrCb -> RGB"))
                if int(Active) == 3:
                    Property.setAttr("value", unicode("RGB -> HSV"))
                if int(Active) == 4:
                    Property.setAttr("value", unicode("HSV -> RGB"))
                if int(Active) == 5:
                    Property.setAttr("value", unicode("RGB -> HLS"))
                if int(Active) == 6:
                    Property.setAttr("value", unicode("HLS -> RGB"))
                if int(Active) == 7:
                    Property.setAttr("value", unicode("RGB -> CIE.XYZ"))
                if int(Active) == 8:
                    Property.setAttr("value", unicode("CIE.XYZ -> RGB"))
                if int(Active) == 9:
                    Property.setAttr("value", unicode("RGB -> CIE.LAB"))
                if int(Active) == 10:
                    Property.setAttr("value", unicode("CIE.LAB -> RGB"))
                if int(Active) == 11:
                    Property.setAttr("value", unicode("RGB -> CIE.LUV"))
                if int(Active) == 12:
                    Property.setAttr("value", unicode("CIE.LUV -> RGB"))

        self.m_oS2iBlockProperties.SetPropertiesXML(self.m_oPropertiesXML)

        self.m_oS2iBlockProperties.SetBorderColor(self.m_oBorderColor)

        self.m_oS2iBlockProperties.SetBackColor(self.m_oBackColor)

        self.widgets['Properties'].destroy()

        # ----------------------------------------------------------------------


# ColorConversionProperties = Properties()
# ColorConversionProperties.show( center=0 )

# ------------------------------------------------------------------------------
# Code generation
# ------------------------------------------------------------------------------
def generate(blockTemplate):
    channels = '3'
    for propIter in blockTemplate.properties:
        if propIter[0] == 'type':
            if propIter[1] == 'RGB -> GRAY':
                code = 'CV_RGB2GRAY'
                channels = '1';
            elif propIter[1] == 'RGB -> YCrCb':
                code = 'CV_RGB2YCrCb'
            elif propIter[1] == 'YCrCb -> RGB':
                code = 'CV_YCrCb2RGB'
            elif propIter[1] == 'RGB -> HSV':
                code = 'CV_RGB2HSV'
            elif propIter[1] == 'HSV -> RGB':
                code = 'CV_HSV2RGB'
            elif propIter[1] == 'RGB -> HLS':
                code = 'CV_RGB2HLS'
            elif propIter[1] == 'HLS -> RGB':
                code = 'CV_HLS2RGB'
            elif propIter[1] == 'RGB -> CIE.XYZ':
                code = 'CV_RGB2XYZ'
            elif propIter[1] == 'CIE.XYZ -> RGB':
                code = 'CV_XYZ2RGB'
            elif propIter[1] == 'RGB -> CIE.LAB':
                code = 'CV_RGB2Lab'
            elif propIter[1] == 'CIE.LAB -> RGB':
                code = 'CV_Lab2RGB'
            elif propIter[1] == 'RGB -> CIE.LUV':
                code = 'CV_RGB2Luv'
            elif propIter[1] == 'CIE.LUV -> RGB':
                code = 'CV_Luv2RGB'
                # Standard
                # else:
                # code = 'CV_RGB2GRAY'
                # channels = '1'
    blockTemplate.imagesIO = \
        'IplImage * block' + blockTemplate.blockNumber + '_img_i1 = NULL;\n' + \
        'IplImage * block' + blockTemplate.blockNumber + '_img_o1 = NULL;\n' + \
        'IplImage * block' + blockTemplate.blockNumber + '_img_t = NULL;\n'
    blockTemplate.functionCall = '\nif(block' + blockTemplate.blockNumber + '_img_i1){\n' + \
                                 'block' + blockTemplate.blockNumber + '_img_o1 = cvCreateImage(cvSize(block' + blockTemplate.blockNumber + \
                                 '_img_i1->width,block' + blockTemplate.blockNumber + '_img_i1->height), block' + blockTemplate.blockNumber + '_img_i1->depth,block' + blockTemplate.blockNumber + '_img_i1->nChannels);\n' + \
                                 'block' + blockTemplate.blockNumber + '_img_t = cvCreateImage(cvSize(block' + blockTemplate.blockNumber + \
                                 '_img_i1->width,block' + blockTemplate.blockNumber + '_img_i1->height), block' + blockTemplate.blockNumber + '_img_i1->depth,' + channels + ');\n' + \
                                 'cvCvtColor(block' + blockTemplate.blockNumber + '_img_i1, block' + blockTemplate.blockNumber + '_img_t ,' + code + ' );}\n' + \
                                 'if ( ' + code + ' == ' + "CV_RGB2GRAY" + ')\n' + \
                                 '{    cvMerge(block' + blockTemplate.blockNumber + '_img_t ,block' + blockTemplate.blockNumber + '_img_t ,block' + blockTemplate.blockNumber + '_img_t ,NULL ,block' + blockTemplate.blockNumber + '_img_o1);\n }\n' + \
                                 'else\n' + '{ block' + blockTemplate.blockNumber + '_img_o1 = cvCloneImage(block' + blockTemplate.blockNumber + '_img_t);\n}'
    blockTemplate.dealloc = 'cvReleaseImage(&block' + blockTemplate.blockNumber + '_img_t);\n' + \
                            'cvReleaseImage(&block' + blockTemplate.blockNumber + '_img_i1);\n' + \
                            'cvReleaseImage(&block' + blockTemplate.blockNumber + '_img_o1);\n'


# ------------------------------------------------------------------------------
# Block Setup
# ------------------------------------------------------------------------------
def getBlock():
    return {"Label": _("Color Conversion"),
            "Path": {"Python": "colorConversion",
                     "Glade": "glade/colorConversion.ui",
                     "Xml": "xml/colorConversion.xml"},
            "Icon": "images/colorConversion.png",
            "Color": "50:125:50:150",
            "InTypes": {0: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "Description": _("Convert colors between different standards of graylevel/color images."),
            "TreeGroup": _("Filters and Color Conversion")
            }
