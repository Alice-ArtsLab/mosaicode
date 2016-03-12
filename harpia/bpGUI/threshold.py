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

        filename = self.m_sDataDir + 'glade/threshold.ui'
        self.m_oPropertiesXML = PropertiesXML
        self.m_oS2iBlockProperties = S2iBlockProperties

        widget_list = [
            'Properties',
            'THREThreshold',
            'THREThresholdType',
            'THRELabelMaxValue',
            'THREMaxValue',
            'BackgroundColor',
            'BorderColor',
            'HelpView'
        ]

        handlers = [
            'on_THREThresholdType_changed',
            'on_BackColorButton_clicked',
            'on_BorderColorButton_clicked',
            'on_cancel_clicked',
            'on_threshold_confirm_clicked',
        ]

        top_window = 'Properties'

        GladeWindow.__init__(self, filename, top_window, widget_list, handlers)

        # load properties values
        self.block_properties = self.m_oPropertiesXML.getTag("properties").getTag("block").getChildTags("property")
        for Property in self.block_properties:

            if Property.name == "threshold":
                self.widgets['THREThreshold'].set_value(float(Property.value))

            if Property.name == "maxValue":
                self.widgets['THREMaxValue'].set_value(float(Property.value))

            if Property.name == "thresholdType":
                if Property.value == "CV_THRESH_BINARY":
                    self.widgets['THREThresholdType'].set_active(int(0))
                    self.on_THREThresholdType_changed()
                if Property.value == "CV_THRESH_BINARY_INV":
                    self.widgets['THREThresholdType'].set_active(int(1))
                    self.on_THREThresholdType_changed()
                if Property.value == "CV_THRESH_TRUNC":
                    self.widgets['THREThresholdType'].set_active(int(2))
                    self.on_THREThresholdType_changed()
                if Property.value == "CV_THRESH_TOZERO":
                    self.widgets['THREThresholdType'].set_active(int(3))
                    self.on_THREThresholdType_changed()
                if Property.value == "CV_THRESH_TOZERO_INV":
                    self.widgets['THREThresholdType'].set_active(int(4))
                    self.on_THREThresholdType_changed()

        self.configure()

        # load help text

        # t_oS2iHelp = XMLParser(self.m_sDataDir + "help/threshold" + _("_en.help"))

        # t_oTextBuffer = gtk.TextBuffer()

        # t_oTextBuffer.set_text(unicode(str(t_oS2iHelp.getTag("help").getTag("content").getTagContent())))

        # self.widgets['HelpView'].set_buffer(t_oTextBuffer)

    #----------------Help Text--------------------------------------

    def getHelp(self):#adicionado help
        return "Operador de binarização da imagem, de acordo com um valor fixo de intensidade luminosa (valor de limiar)."

    # ----------------------------------------------------------------------

    def __del__(self):

        pass

    # ----------------------------------------------------------------------

    def on_threshold_confirm_clicked(self, *args):

        for Property in self.block_properties:

            if Property.name == "threshold":
                Property.value = unicode(self.widgets['THREThreshold'].get_value())

            if Property.name == "maxValue":
                Property.value = unicode(self.widgets['THREMaxValue'].get_value())

            if Property.name == "thresholdType":
                Active = self.widgets['THREThresholdType'].get_active()
                if int(Active) == 0:
                    Property.value = unicode("CV_THRESH_BINARY")
                if int(Active) == 1:
                    Property.value = unicode("CV_THRESH_BINARY_INV")
                if int(Active) == 2:
                    Property.value = unicode("CV_THRESH_TRUNC")
                if int(Active) == 3:
                    Property.value = unicode("CV_THRESH_TOZERO")
                if int(Active) == 4:
                    Property.value = unicode("CV_THRESH_TOZERO_INV")

        self.m_oS2iBlockProperties.SetPropertiesXML(self.m_oPropertiesXML)

        self.m_oS2iBlockProperties.SetBorderColor(self.m_oBorderColor)

        self.m_oS2iBlockProperties.SetBackColor(self.m_oBackColor)

        self.widgets['Properties'].destroy()

    # ----------------------------------------------------------------------

    def on_THREThresholdType_changed(self, *args):

        Active = self.widgets['THREThresholdType'].get_active()
        if int(Active) == 0 or int(Active) == 1:
            self.widgets['THRELabelMaxValue'].set_sensitive(True)
            self.widgets['THREMaxValue'].set_sensitive(True)
        else:
            self.widgets['THRELabelMaxValue'].set_sensitive(False)
            self.widgets['THREMaxValue'].set_sensitive(False)

            # ----------------------------------------------------------------------


# ThresholdProperties = Properties()
# ThresholdProperties.show( center=0 )

# ------------------------------------------------------------------------------
# Code generation
# ------------------------------------------------------------------------------
def generate(blockTemplate):
    for propIter in blockTemplate.properties:
        if propIter[0] == 'threshold':
            thresholdValue = propIter[1]
        elif propIter[0] == 'maxValue':
            maxValue = propIter[1]
        elif propIter[0] == 'thresholdType':
            thresholdType = propIter[1]

    blockTemplate.imagesIO = \
        'IplImage * block$$_img_i1 = NULL;\n' + \
        'IplImage * block$$_img_o1 = NULL;\n'
    blockTemplate.functionArguments = \
        'int block$$_arg_threshold = ' + thresholdValue + ';\n' + \
        'int block$$_arg_maxValue = ' + maxValue + ';\n' + \
        'int block$$_arg_thresholdType = ' + thresholdType + ';\n'
    blockTemplate.functionCall = '\nif(block$$_img_i1){\n' + \
                                 'block$$_img_o1 = cvCreateImage(cvSize(block' + $$ + \
                                 '_img_i1->width,block$$_img_i1->height),block' + $$ + \
                                 '_img_i1->depth,block$$_img_i1->nChannels);\n' + \
                                 '\ncvThreshold(block$$_img_i1,block' + $$ + \
                                 '_img_o1,block$$_arg_threshold,block' + $$ + \
                                 '_arg_maxValue,block$$_arg_thresholdType);}\n'
    blockTemplate.dealloc = 'cvReleaseImage(&block$$_img_o1);\n' + \
                            'cvReleaseImage(&block$$_img_i1);\n'


# ------------------------------------------------------------------------------
# Block Setup
# ------------------------------------------------------------------------------
def getBlock():
    return {"Label": _("Threshold"),
            "Path": {"Python": "threshold",
                     "Glade": "glade/threshold.ui",
                     "Xml": "xml/threshold.xml"},
            "Icon": "images/threshold.png",
            "Color": "50:125:50:150",
            "InTypes": {0: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "Description": _("Image binarization operator, according to a fixed threshold value."),
            "TreeGroup": _("Filters and Color Conversion")
            }
