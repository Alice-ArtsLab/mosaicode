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

        filename = self.m_sDataDir + 'glade/matchTem.ui'
        self.m_oPropertiesXML = PropertiesXML
        self.m_oS2iBlockProperties = S2iBlockProperties

        widget_list = [
            'Properties',
            'method',
            'scaleFactor',
            'BackgroundColor',
            'BorderColor',
            'HelpView'
        ]

        handlers = [
            'on_cancel_clicked',
            'on_prop_confirm_clicked',
            'on_BackColorButton_clicked',
            'on_BorderColorButton_clicked'
        ]

        top_window = 'Properties'

        GladeWindow.__init__(self, filename, top_window, widget_list, handlers)


        # load properties values
        self.block_properties = self.m_oPropertiesXML.getTag("properties").getTag("block").getChildTags("property")
        for Property in self.block_properties:
            if Property.name == "scaleFactor":
                self.widgets['scaleFactor'].set_value(float(Property.value));
            if Property.name == "method":
                if Property.value == "CV_TM_CCOEFF_NORMED":
                    self.widgets['method'].set_active(int(0))
                if Property.value == "CV_TM_CCOEFF":
                    self.widgets['method'].set_active(int(1))
                if Property.value == "CV_TM_CCORR_NORMED":
                    self.widgets['method'].set_active(int(2))
                if Property.value == "CV_TM_CCORR":
                    self.widgets['method'].set_active(int(3))
                if Property.value == "CV_TM_SQDIFF_NORMED":
                    self.widgets['method'].set_active(int(4))
                if Property.value == "CV_TM_SQDIFF":
                    self.widgets['method'].set_active(int(5))

        self.configure()

        # load help text
        # t_oS2iHelp = XMLParser(self.m_sDataDir + "help/checkCir" + _("_en.help"))

        # t_oTextBuffer = gtk.TextBuffer()

        # t_oTextBuffer.set_text(unicode(str(t_oS2iHelp.getTag("help").getTag("content").getTagContent())))

        # self.widgets['HelpView'].set_buffer(t_oTextBuffer)

    # ----------------------------------------------------------------------
    def getHelp(self):
        return "operação de filtragem destinada a suavizar uma imagem."

    # ----------------------------------------------------------------------

    def __del__(self):
        pass

    # ----------------------------------------------------------------------

    def on_prop_confirm_clicked(self, *args):

        for Property in self.block_properties:
            if Property.name == "scaleFactor":
                Property.value = unicode(self.widgets['scaleFactor'].get_value())
            if Property.name == "method":
                Active = self.widgets['method'].get_active()
                if int(Active) == 0:
                    Property.value = unicode("CV_TM_CCOEFF_NORMED")
                if int(Active) == 1:
                    Property.value = unicode("CV_TM_CCOEFF")
                if int(Active) == 2:
                    Property.value = unicode("CV_TM_CCORR_NORMED")
                if int(Active) == 3:
                    Property.value = unicode("CV_TM_CCORR")
                if int(Active) == 4:
                    Property.value = unicode("CV_TM_SQDIFF_NORMED")
                if int(Active) == 5:
                    Property.value = unicode("CV_TM_SQDIFF")

        self.m_oS2iBlockProperties.SetPropertiesXML(self.m_oPropertiesXML)

        self.m_oS2iBlockProperties.SetBorderColor(self.m_oBorderColor)
        self.m_oS2iBlockProperties.SetBackColor(self.m_oBackColor)
        self.widgets['Properties'].destroy()

    # ----------------------------------------------------------------------


# propProperties = Properties()()
# propProperties.show( center=0 )

# ------------------------------------------------------------------------------
# Code generation
# ------------------------------------------------------------------------------
def generate(blockTemplate):
    for propIter in blockTemplate.properties:
        if propIter[0] == 'method':
            interMethod = propIter[1]
        if propIter[0] == "scaleFactor":
            scaleFactor = propIter[1]

    blockTemplate.imagesIO = \
        'IplImage * block' + blockTemplate.blockNumber + '_img_i1 = NULL;\n' + \
        'IplImage * block' + blockTemplate.blockNumber + '_img_i2 = NULL;\n' + \
        'IplImage * block' + blockTemplate.blockNumber + '_img_t1 = NULL;\n' + \
        'IplImage * block' + blockTemplate.blockNumber + '_img_o1 = NULL;\n'
    blockTemplate.functionCall = '\nif(block' + blockTemplate.blockNumber + '_img_i1 && block' + blockTemplate.blockNumber + '_img_i2)\n' + \
                                 '{\n' + \
                                 '	block' + blockTemplate.blockNumber + '_img_t1 = cvCreateImage(cvSize(block' + blockTemplate.blockNumber + '_img_i1->width - block' + blockTemplate.blockNumber + '_img_i2->width +1,block' + blockTemplate.blockNumber + '_img_i1->height - block' + blockTemplate.blockNumber + '_img_i2->height +1),32,1);\n' + \
                                 '	block' + blockTemplate.blockNumber + '_img_o1 = cvCreateImage(cvSize(block' + blockTemplate.blockNumber + '_img_i1->width - block' + blockTemplate.blockNumber + '_img_i2->width +1,block' + blockTemplate.blockNumber + '_img_i1->height - block' + blockTemplate.blockNumber + '_img_i2->height +1),8,1);\n' + \
                                 '	cvMatchTemplate(block' + blockTemplate.blockNumber + '_img_i1 , block' + blockTemplate.blockNumber + '_img_i2, block' + blockTemplate.blockNumber + '_img_t1, ' + interMethod + ');\n' + \
                                 '	cvConvertScale(block' + blockTemplate.blockNumber + '_img_t1,block' + blockTemplate.blockNumber + '_img_o1, ' + str(
        10 ** -(int(float(scaleFactor)))) + ',0);\n' + \
                                 '}\n'
    blockTemplate.dealloc = 'cvReleaseImage(&block' + blockTemplate.blockNumber + '_img_o1);\n' + \
                            'cvReleaseImage(&block' + blockTemplate.blockNumber + '_img_t1);\n' + \
                            'cvReleaseImage(&block' + blockTemplate.blockNumber + '_img_i2);\n' + \
                            'cvReleaseImage(&block' + blockTemplate.blockNumber + '_img_i1);\n'


# ------------------------------------------------------------------------------
# Block Setup
# ------------------------------------------------------------------------------
def getBlock():
    return {"Label": _("Match Template"),
            "Path": {"Python": "matchTem",
                     "Glade": "glade/matchTem.ui",
                     "Xml": "xml/matchTem.xml"},
            "Inputs": 2,
            "Outputs": 1,
            "Icon": "images/matchTem.png",
            "Color": "180:180:10:150",
            "InTypes": {0: "HRP_IMAGE", 1: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "Description": _("Output shows the matching relation between image (input1) and template (input2)"),
            "TreeGroup": _("Feature Detection")
            }
