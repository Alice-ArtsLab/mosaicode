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

from harpia.GladeWindow import GladeWindow
from harpia.amara import binderytools as bt
import gtk
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

        filename = self.m_sDataDir + 'glade/equalizeHistogram.ui'
        self.m_oPropertiesXML = PropertiesXML
        self.m_oS2iBlockProperties = S2iBlockProperties

        widget_list = [
            'Properties',
            'BackgroundColor',
            'BorderColor',
            'HelpView'
        ]

        handlers = [
            #  'on_EQUARadioAutomatic_pressed',
            #  'on_EQUARadioBand_pressed',
            'on_BackColorButton_clicked',
            'on_BorderColorButton_clicked',
            'on_cancel_clicked',
            'on_equalizeHistogram_confirm_clicked'
        ]

        top_window = 'Properties'

        GladeWindow.__init__(self, filename, top_window, widget_list, handlers)

        self.configure()

        # load help text
        t_oS2iHelp = XMLParser(self.m_sDataDir + "help/equalizeHistogram" + _("_en.help"))

        t_oTextBuffer = gtk.TextBuffer()

        t_oTextBuffer.set_text(unicode(str(t_oS2iHelp.getTag("help").getTag("content").getTagContent())))

        self.widgets['HelpView'].set_buffer(t_oTextBuffer)

    # ----------------------------------------------------------------------

    def __del__(self):
        pass

    # ----------------------------------------------------------------------

    def on_equalizeHistogram_confirm_clicked(self, *args):
        # self.m_oPropertiesXML.properties.block.property[0].name = unicode("type")
        # self.m_oPropertiesXML.properties.block.property[1].name = unicode("min")
        # self.m_oPropertiesXML.properties.block.property[2].name = unicode("max")

        #  for Property in self.m_oPropertiesXML.properties.block.property:

        #      if Property.name == "type":
        #          if self.widgets['EQUARadioBand'].get_active( ):
        #              Property.value = unicode( "band" )
        #          else:
        #              Property.value = unicode( "automatic" )

        #      if Property.name == "min":
        #          Property.value = unicode( str( int(self.widgets['EQUAMinBand'].get_value( ) ) ) )

        #      if Property.name == "max":
        #          Property.value = unicode( str( int( self.widgets['EQUAMaxBand'].get_value( ) )))

        self.m_oS2iBlockProperties.SetPropertiesXML(self.m_oPropertiesXML)

        self.m_oS2iBlockProperties.SetBorderColor(self.m_oBorderColor)

        self.m_oS2iBlockProperties.SetBackColor(self.m_oBackColor)

        self.widgets['Properties'].destroy()

        # ----------------------------------------------------------------------


        # def on_EQUARadioAutomatic_pressed(self, *args ):

        #     self.widgets['EQUALabelMin'].set_sensitive( False )
        #     self.widgets['EQUAMinBand'].set_sensitive( False )
        #     self.widgets['EQUALabelMax'].set_sensitive( False )
        #     self.widgets['EQUAMaxBand'].set_sensitive( False )

        # ----------------------------------------------------------------------

        # def on_EQUARadioBand_pressed(self, *args ):

        #    self.widgets['EQUALabelMin'].set_sensitive( True )
        #    self.widgets['EQUAMinBand'].set_sensitive( True )
        #    self.widgets['EQUALabelMax'].set_sensitive( True )
        #    self.widgets['EQUAMaxBand'].set_sensitive( True )

        # ----------------------------------------------------------------------


# EqualizeHistogramProperties = Properties()
# EqualizeHistogramProperties.show( center=0 )

# ------------------------------------------------------------------------------
# Code generation
# ------------------------------------------------------------------------------
def generate(blockTemplate):
    blockTemplate.imagesIO = \
        'IplImage * block' + blockTemplate.blockNumber + '_img_i1 = NULL;\n' + \
        'IplImage * block' + blockTemplate.blockNumber + '_img_o1 = NULL;\n' + \
        'IplImage * block' + blockTemplate.blockNumber + '_SourceCx[3];\n' + \
        'IplImage * block' + blockTemplate.blockNumber + '_EqCx[3];\n'
    blockTemplate.functionCall = '\nif(block' + blockTemplate.blockNumber + '_img_i1){\n' + \
                                 'block' + blockTemplate.blockNumber + '_img_o1 = cvCreateImage(cvSize(block' + blockTemplate.blockNumber + \
                                 '_img_i1->width,block' + blockTemplate.blockNumber + '_img_i1->height), IPL_DEPTH_8U, 3);\n' + \
                                 'block' + blockTemplate.blockNumber + '_SourceCx[0] = cvCreateImage(cvSize(block' + blockTemplate.blockNumber + \
                                 '_img_i1->width,block' + blockTemplate.blockNumber + '_img_i1->height), IPL_DEPTH_8U, 1);\n' + \
                                 'block' + blockTemplate.blockNumber + '_SourceCx[1] = cvCreateImage(cvSize(block' + blockTemplate.blockNumber + \
                                 '_img_i1->width,block' + blockTemplate.blockNumber + '_img_i1->height), IPL_DEPTH_8U, 1);\n' + \
                                 'block' + blockTemplate.blockNumber + '_SourceCx[2] = cvCreateImage(cvSize(block' + blockTemplate.blockNumber + \
                                 '_img_i1->width,block' + blockTemplate.blockNumber + '_img_i1->height), IPL_DEPTH_8U, 1);\n' + \
                                 'block' + blockTemplate.blockNumber + '_EqCx[0] = cvCreateImage(cvSize(block' + blockTemplate.blockNumber + \
                                 '_img_i1->width,block' + blockTemplate.blockNumber + '_img_i1->height), IPL_DEPTH_8U, 1);\n' + \
                                 'block' + blockTemplate.blockNumber + '_EqCx[1] = cvCreateImage(cvSize(block' + blockTemplate.blockNumber + \
                                 '_img_i1->width,block' + blockTemplate.blockNumber + '_img_i1->height), IPL_DEPTH_8U, 1);\n' + \
                                 'block' + blockTemplate.blockNumber + '_EqCx[2] = cvCreateImage(cvSize(block' + blockTemplate.blockNumber + \
                                 '_img_i1->width,block' + blockTemplate.blockNumber + '_img_i1->height), IPL_DEPTH_8U, 1);\n' + \
                                 'cvSplit(block' + blockTemplate.blockNumber + '_img_i1,block' + blockTemplate.blockNumber + '_SourceCx[0],' + \
                                 'block' + blockTemplate.blockNumber + '_SourceCx[1],block' + blockTemplate.blockNumber + '_SourceCx[2], NULL);\n' + \
                                 'cvEqualizeHist(block' + blockTemplate.blockNumber + '_SourceCx[0], block' + blockTemplate.blockNumber + '_EqCx[0]);\n' + \
                                 'cvEqualizeHist(block' + blockTemplate.blockNumber + '_SourceCx[1], block' + blockTemplate.blockNumber + '_EqCx[1]);\n' + \
                                 'cvEqualizeHist(block' + blockTemplate.blockNumber + '_SourceCx[2], block' + blockTemplate.blockNumber + '_EqCx[2]);\n' + \
                                 'cvMerge( block' + blockTemplate.blockNumber + '_EqCx[0],block' + blockTemplate.blockNumber + '_EqCx[1],' + \
                                 'block' + blockTemplate.blockNumber + '_EqCx[2], NULL,block' + blockTemplate.blockNumber + '_img_o1);\n' + \
                                 'cvReleaseImage(&block' + blockTemplate.blockNumber + '_SourceCx[0]);\n' + \
                                 'cvReleaseImage(&block' + blockTemplate.blockNumber + '_SourceCx[1]);\n' + \
                                 'cvReleaseImage(&block' + blockTemplate.blockNumber + '_SourceCx[2]);\n' + \
                                 'cvReleaseImage(&block' + blockTemplate.blockNumber + '_EqCx[0]);\n' + \
                                 'cvReleaseImage(&block' + blockTemplate.blockNumber + '_EqCx[1]);\n' + \
                                 'cvReleaseImage(&block' + blockTemplate.blockNumber + '_EqCx[2]);\n' + \
                                 '}\n'
    blockTemplate.dealloc = 'cvReleaseImage(&block' + blockTemplate.blockNumber + '_img_o1);\n' + \
                            'cvReleaseImage(&block' + blockTemplate.blockNumber + '_img_i1);\n'


# ------------------------------------------------------------------------------
# Block Setup
# ------------------------------------------------------------------------------
def getBlock():
    return {"Label": _("Equalize Histogram"),
            "Path": {"Python": "equalizeHistogram",
                     "Glade": "glade/equalizeHistogram.ui",
                     "Xml": "xml/equalizeHistogram.xml"},
            "Inputs": 1,
            "Outputs": 1,
            "Icon": "images/equalizeHistogram.png",
            "Color": "0:0:0:150",
            "InTypes": {0: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "Description": _(
                "The histogram equalization of an image intends to reinforce contrast of the image elements."),
            "TreeGroup": _("Histograms")
            }
