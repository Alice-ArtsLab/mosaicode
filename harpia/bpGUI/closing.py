# -*- coding: utf-8 -*-
# [HARPIA PROJECT]
#[Ourobolos Project UFSJ]
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

        filename = self.m_sDataDir + 'glade/closing.ui'
        self.m_oPropertiesXML = PropertiesXML
        self.m_oS2iBlockProperties = S2iBlockProperties

        widget_list = [
            'Properties',
            'CLOSMaskSize',
            'BackgroundColor',
            'BorderColor',
            'HelpView',
            'closing_confirm'
        ]

        handlers = [
            'on_BackColorButton_clicked',
            'on_BorderColorButton_clicked',
            'on_cancel_clicked',
            'on_closing_confirm_clicked'
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
                    self.widgets['CLOSMaskSize'].set_active(int(0))
                if value == "5x5":
                    self.widgets['CLOSMaskSize'].set_active(int(1))
                if value == "7x7":
                    self.widgets['CLOSMaskSize'].set_active(int(2))

        self.configure()

        # # load help text
        # t_oS2iHelp = XMLParser(self.m_sDataDir + "help/closing" + _("_en.help"))

        # t_oTextBuffer = gtk.TextBuffer()

        # t_oTextBuffer.set_text(unicode(str(t_oS2iHelp.getTag("help").getTag("content").getTagContent())))

        # self.widgets['HelpView'].set_buffer(t_oTextBuffer)

    # ----------------------------------------------------------------------

    def __del__(self):
        pass

    # ----------------------------------------------------------------------

    def on_closing_confirm_clicked(self, *args):
        self.widgets['closing_confirm'].grab_focus()
        for Property in self.block_properties:

            name = Property.getAttr("name")
            value = Property.getAttr("value")

            if name == "masksize":
                Active = self.widgets['CLOSMaskSize'].get_active()
                if int(Active) == 0:
                   Property.setAttr("value",  unicode("3x3"))
                if int(Active) == 1:
                   Property.setAttr("value",  unicode("5x5"))
                if int(Active) == 2:
                   Property.setAttr("value",  unicode("7x7"))

        self.m_oS2iBlockProperties.SetPropertiesXML(self.m_oPropertiesXML)

        self.m_oS2iBlockProperties.SetBorderColor(self.m_oBorderColor)

        self.m_oS2iBlockProperties.SetBackColor(self.m_oBackColor)

        self.widgets['Properties'].destroy()

        # ----------------------------------------------------------------------

    def getHelp(self):
        return"Operação de morfologia matemática para realizar a fechamento da imagem de acordo com o elemento estruturante. Equivale a aplicação de uma dilatação seguida de uma erosão."

# ------------------------------------------------------------------------------
# Code generation
# ------------------------------------------------------------------------------
def generate(blockTemplate):
    for propIter in blockTemplate.properties:
        if propIter[0] == 'masksize':
            maskSizeValue = propIter[1]
    blockTemplate.imagesIO = \
        'IplImage * block$$_img_i1 = NULL;\n' + \
        'IplImage * block$$_img_o1 = NULL;\n'
    blockTemplate.imagesIO += 'IplConvKernel * block$$' +\
                                      '_arg_mask = cvCreateStructuringElementEx(' + maskSizeValue[0] + ' , ' + \
                                      maskSizeValue[2] + ', 1, 1,CV_SHAPE_RECT,NULL);\n'
    blockTemplate.functionCall = '\nif(block$$_img_i1){\n' + \
                                 'IplImage * block$$_auxImg;' + \
                                 'block$$_img_o1 = cvCreateImage(cvSize(block$$' +\
                                 '_img_i1->width, block$$_img_i1->height), block$$' +\
                                 '_img_i1->depth ,block$$_img_i1->nChannels);\n' + \
                                 '\nblock$$_auxImg = cvCreateImage(cvSize(block$$' +\
                                 '_img_i1->width, block$$_img_i1->height), block$$' +\
                                 '_img_i1->depth ,block$$_img_i1->nChannels);\n' + \
                                 'cvMorphologyEx(block$$_img_i1,block$$_img_o1,NULL,' + \
                                 'block$$_arg_mask, CV_MOP_CLOSE, 1);\n}\n'
    blockTemplate.dealloc = 'cvReleaseImage(&block$$_img_o1);\n' + \
                            'cvReleaseStructuringElement(&block$$_arg_mask);\n' + \
                            'cvReleaseImage(&block$$_img_i1);\n'


# ------------------------------------------------------------------------------
# Block Setup
# ------------------------------------------------------------------------------
def getBlock():
    return {"Label": _("Closing"),
            "Path": {"Python": "closing",
                     "Glade": "glade/closing.ui",
                     "Xml": "xml/closing.xml"},
            "Icon": "images/closing.png",
            "Color": "180:230:220:150",
            "InTypes": {0: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "Description": _("Morphological operation that connects objects on an image."),
            "TreeGroup": _("Morphological Operations")
            }
