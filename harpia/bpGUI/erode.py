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

        filename = self.m_sDataDir + 'glade/erode.ui'
        self.m_oPropertiesXML = PropertiesXML
        self.m_oS2iBlockProperties = S2iBlockProperties

        widget_list = [
            'Properties',
            'ERODMaskSize',
            'ERODIterations',
            'BackgroundColor',
            'BorderColor',
            'HelpView',
            'erode_confirm'
        ]

        handlers = [
            'on_cancel_clicked',
            'on_erode_confirm_clicked',
            'on_BorderColorButton_clicked',
            'on_BackColorButton_clicked'
        ]

        top_window = 'Properties'

        GladeWindow.__init__(self, filename, top_window, widget_list, handlers)

        self.block_properties = self.m_oPropertiesXML.getTag("properties").getTag("block").getChildTags("property")
        # load properties values
        for Property in self.block_properties:

            name = Property.getAttr("name")
            value = Property.getAttr("value")

            if name == "masksize":
                if value == "3x3":
                    self.widgets['ERODMaskSize'].set_active(int(0))
                if value == "5x5":
                    self.widgets['ERODMaskSize'].set_active(int(1))
                if value == "7x7":
                    self.widgets['ERODMaskSize'].set_active(int(2))

            if name == "iterations":
                self.widgets['ERODIterations'].set_value(int(value))

        self.configure()

        # load help text
        t_oS2iHelp = XMLParser(self.m_sDataDir + "help/erode" + _("_en.help"))

        t_oTextBuffer = gtk.TextBuffer()

        t_oTextBuffer.set_text(unicode(str(t_oS2iHelp.getTag("help").getTag("content").getTagContent())))

        self.widgets['HelpView'].set_buffer(t_oTextBuffer)

    # ----------------------------------------------------------------------

    def __del__(self):
        pass

    # ----------------------------------------------------------------------

    def on_erode_confirm_clicked(self, *args):
        self.widgets['erode_confirm'].grab_focus()

        for Property in self.block_properties:

            name = Property.getAttr("name")

            if name == "masksize":
                Active = self.widgets['ERODMaskSize'].get_active()
                if int(Active) == 0:
                    Property.setAttr("value", "3x3")
                if int(Active) == 1:
                    Property.setAttr("value", "5x5")
                if int(Active) == 2:
                    Property.setAttr("value", "7x7")

            if name == "iterations":
                Property.setAttr("value", str(int(self.widgets['ERODIterations'].get_value())))

        self.m_oS2iBlockProperties.SetPropertiesXML(self.m_oPropertiesXML)

        self.m_oS2iBlockProperties.SetBorderColor(self.m_oBorderColor)

        self.m_oS2iBlockProperties.SetBackColor(self.m_oBackColor)

        self.widgets['Properties'].destroy()

        # ----------------------------------------------------------------------


# ErodeProperties = Properties()
# ErodeProperties.show( center=0 )

# ------------------------------------------------------------------------------
# Code generation
# ------------------------------------------------------------------------------
def generate(blockTemplate):
    for propIter in blockTemplate.properties:
        if propIter[0] == 'masksize':
            maskSizeValue = propIter[1]
        elif propIter[0] == 'iterations':
            iterationsValue = propIter[1]
    blockTemplate.imagesIO = "// ERODE input and output\n"
    blockTemplate.imagesIO += \
        'IplImage * block' + blockTemplate.blockNumber + '_img_i1 = NULL; // ERODE input\n' + \
        'IplImage * block' + blockTemplate.blockNumber + '_img_o1 = NULL; // ERODE output\n'
    blockTemplate.imagesIO += '\n\n'

    blockTemplate.functionArguments = 'int block' + blockTemplate.blockNumber + '_arg_iterations = ' + \
                                      iterationsValue + ';\n'
    blockTemplate.functionArguments += 'IplConvKernel * block' + blockTemplate.blockNumber + \
                                       '_arg_mask = cvCreateStructuringElementEx(' + maskSizeValue[0] + \
                                       ' , ' + maskSizeValue[2] + ', 1, 1,CV_SHAPE_RECT,NULL);\n'

    blockTemplate.functionCall = '\nif(block' + blockTemplate.blockNumber + '_img_i1){\n' + \
                                 'block' + blockTemplate.blockNumber + '_img_o1 = cvCreateImage(cvSize(block' + blockTemplate.blockNumber + \
                                 '_img_i1->width, block' + blockTemplate.blockNumber + '_img_i1->height), block' + blockTemplate.blockNumber + \
                                 '_img_i1->depth ,block' + blockTemplate.blockNumber + '_img_i1->nChannels);\n' + \
                                 '\ncvErode(block' + blockTemplate.blockNumber + '_img_i1,block' + blockTemplate.blockNumber + \
                                 '_img_o1,block' + blockTemplate.blockNumber + '_arg_mask,block' + blockTemplate.blockNumber + \
                                 '_arg_iterations);\n}\n'

    blockTemplate.dealloc = 'cvReleaseImage(&block' + blockTemplate.blockNumber + '_img_o1); // ERODE input\n' + \
                            'cvReleaseImage(&block' + blockTemplate.blockNumber + '_img_i1); // ERODE output\n'


# ------------------------------------------------------------------------------
# Block Setup
# ------------------------------------------------------------------------------
def getBlock():
    return {"Label": _("Erosion"),
            "Path": {"Python": "erode",
                     "Glade": "glade/erode.ui",
                     "Xml": "xml/erode.xml"},
            "Inputs": 1,
            "Outputs": 1,
            "Icon": "images/erode.png",
            "Color": "180:230:220:150",
            "InTypes": {0: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "Description": _("Morphological operation that erodes the objects of the image, reducing their size."),
            "TreeGroup": _("Morphological Operations")
            }
