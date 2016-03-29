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

        filename = self.m_sDataDir + 'glade/canny.ui'
        self.m_oPropertiesXML = PropertiesXML
        self.m_oS2iBlockProperties = S2iBlockProperties

        widget_list = [
            'Properties',
            'CANNThreshold1',
            'CANNThreshold2',
            'CANNApertureSize',
            'BackgroundColor',
            'BorderColor',
            'HelpView',
            'canny_confirm'
        ]

        handlers = [
            'on_BackColorButton_clicked',
            'on_BorderColorButton_clicked',
            'on_cancel_clicked',
            'on_canny_confirm_clicked'
        ]

        top_window = 'Properties'

        GladeWindow.__init__(self, filename, top_window, widget_list, handlers)

        block_properties = self.m_oPropertiesXML.getTag("properties").getTag("block").getChildTags("property")

        # load properties values
        for Property in block_properties:
            name = Property.getAttr("name")
            value = Property.getAttr("value")

            if name == "threshold1":
                self.widgets['CANNThreshold1'].set_value(float(value))

            if name == "threshold2":
                self.widgets['CANNThreshold2'].set_value(float(value))

            if name == "apertureSize":
                #  if Property.value == "1":
                #      self.widgets['CANNApertureSize'].set_active( int(0) )
                if value == "3":
                    self.widgets['CANNApertureSize'].set_active(int(0))
                if value == "5":
                    self.widgets['CANNApertureSize'].set_active(int(1))
                if value == "7":
                    self.widgets['CANNApertureSize'].set_active(int(2))

        self.configure()
       
    
        #----------------------------------------------------------------
        # # # load help text -- Commit Carlos 
        # t_oS2iHelp = XMLParser(self.m_sDataDir + "help/canny" + _("_en.help"))

        # t_oTextBuffer = gtk.TextBuffer()

        # t_oTextBuffer.set_text(unicode(str(t_oS2iHelp.getTag("help").getTag("content").getTagContent())))

        # self.widgets['HelpView'].set_buffer(t_oTextBuffer)
    

    # ----------------------------------------------------------------------

    def __del__(self):

        pass

    # ----------------------------------------------------------------------

    def on_canny_confirm_clicked(self, *args):
        self.widgets['canny_confirm'].grab_focus()

        block_properties = self.m_oPropertiesXML.getTag("properties").getTag("block").getChildTags("property")

        for Property in block_properties:

            name = Property.getAttr("name")
            value = Property.getAttr("value")

            if name == "threshold1":
                Property.setAttr("value", self.widgets['CANNThreshold1'].get_value())

            if name == "threshold2":
                Property.setAttr("value",self.widgets['CANNThreshold2'].get_value())

            if name == "apertureSize":
                Active = self.widgets['CANNApertureSize'].get_active()
                # if int(Active) == 0:
                #    Property.value = unicode("1")
                if int(Active) == 0:
                    Property.setAttr("value", "3")
                if int(Active) == 1:
                    Property.setAttr("value", "5")
                if int(Active) == 2:
                    Property.setAttr("value", "7")


        self.m_oS2iBlockProperties.SetPropertiesXML(self.m_oPropertiesXML)
        self.m_oS2iBlockProperties.SetBorderColor(self.m_oBorderColor)
        self.m_oS2iBlockProperties.SetBackColor(self.m_oBackColor)
        self.widgets['Properties'].destroy()

        # ----------------------------------------------------------------------
        #help function -- 
    def getHelp(self):
        return "Operacão de filtragem que implementa o algoritmo Canny para detecção de contornos e bordas.\nPropriedades\nLimiar 1 e Limiar 2: os dois valores de limiar são utilizados em conjunto. O menor valor é utilizado para a realizar a conexão de cantos e bordas. O maior valor é utilizado para encontrar segmentos iniciais das bordas mais significativas."



# CannyProperties = Properties()
# CannyProperties.show( center=0 )


#GetHelp generation

# ------------------------------------------------------------------------------
# Code generation
# ------------------------------------------------------------------------------
def generate(blockTemplate):
    for propIter in blockTemplate.properties:
        if propIter[0] == 'threshold2':
            threshold2Value = propIter[1]
        elif propIter[0] == 'apertureSize':
            apertureSizeValue = propIter[1]
        elif propIter[0] == 'threshold1':
            threshold1Value = propIter[1]
    blockTemplate.imagesIO = \
        'IplImage * block' + blockTemplate.blockNumber + '_img_i1 = NULL;\nIplImage * block' + blockTemplate.blockNumber + '_img_o1 = NULL;\n'
    blockTemplate.functionArguments = \
        'int block' + blockTemplate.blockNumber + '_arg_threshold2 = ' + threshold2Value + \
        ';\nint block' + blockTemplate.blockNumber + '_arg_aperture_size = ' + apertureSizeValue + \
        ';\nint block' + blockTemplate.blockNumber + '_arg_threshold1 = ' + threshold1Value + ';\n'
    blockTemplate.functionCall = '\nif(block' + blockTemplate.blockNumber + '_img_i1){\n' + \
                                 'block' + blockTemplate.blockNumber + '_img_o1 = cvCreateImage(cvSize(block' + blockTemplate.blockNumber + \
                                 '_img_i1->width,block' + blockTemplate.blockNumber + '_img_i1->height),block' + blockTemplate.blockNumber + \
                                 '_img_i1->depth,block' + blockTemplate.blockNumber + '_img_i1->nChannels);\n IplImage * tmpImg' + blockTemplate.blockNumber + \
                                 ' = cvCreateImage(cvGetSize(block' + blockTemplate.blockNumber + '_img_i1),8,1);\n if(block' + blockTemplate.blockNumber + \
                                 '_img_i1->nChannels == 3)\n {cvCvtColor(block' + blockTemplate.blockNumber + '_img_i1,tmpImg' + blockTemplate.blockNumber + \
                                 ',CV_RGB2GRAY);}\n else\n{tmpImg' + blockTemplate.blockNumber + ' = block' + blockTemplate.blockNumber + \
                                 '_img_i1 = NULL;}\n cvCanny(tmpImg' + blockTemplate.blockNumber + ', tmpImg' + blockTemplate.blockNumber + \
                                 ', block' + blockTemplate.blockNumber + '_arg_threshold1, block' + blockTemplate.blockNumber + \
                                 '_arg_threshold2, block' + blockTemplate.blockNumber + '_arg_aperture_size);\n' + \
                                 'if(block' + blockTemplate.blockNumber + '_img_i1->nChannels == 3)\n{cvCvtColor(tmpImg' + blockTemplate.blockNumber + \
                                 ', block' + blockTemplate.blockNumber + '_img_o1,CV_GRAY2RGB);}\nelse\n{cvCopyImage(tmpImg' + blockTemplate.blockNumber + \
                                 ', block' + blockTemplate.blockNumber + '_img_o1);}\ncvReleaseImage(&tmpImg' + blockTemplate.blockNumber + ');}\n'
    blockTemplate.dealloc = 'cvReleaseImage(&block' + blockTemplate.blockNumber + '_img_o1);\n' + \
                            'cvReleaseImage(&block' + blockTemplate.blockNumber + '_img_i1);\n'


# ------------------------------------------------------------------------------
# Block Setup
# ------------------------------------------------------------------------------
def getBlock():
    return {"Label": _("Canny"),
            "Path": {"Python": "canny",
                     "Glade": "glade/canny.ui",
                     "Xml": "xml/canny.xml"},
            "Icon": "images/canny.png",
            "Color": "250:180:80:150",
            "InTypes": {0: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "Description": _("Filtering operation that employs the Canny algorithm to detect edges."),
            "TreeGroup": _("Gradients, Edges and Corners")
            }
