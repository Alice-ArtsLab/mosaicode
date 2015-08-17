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

        filename = self.m_sDataDir + 'glade/minMax.ui'
        self.m_oPropertiesXML = PropertiesXML
        self.m_oS2iBlockProperties = S2iBlockProperties

        widget_list = [
            'Properties',
            'minX',
            'maxX',
            'minY',
            'maxY',
            'minVal',
            'maxVal',
            'min',
            'max',
            'Pos',
            'Val',
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
            if Property.name == "minX":
                self.widgets['minX'].set_value(float(Property.value));
            if Property.name == "maxX":
                self.widgets['maxX'].set_value(float(Property.value));
            if Property.name == "minY":
                self.widgets['minY'].set_value(float(Property.value));
            if Property.name == "maxY":
                self.widgets['maxY'].set_value(float(Property.value));
            if Property.name == "minVal":
                self.widgets['minVal'].set_value(float(Property.value));
            if Property.name == "maxVal":
                self.widgets['maxVal'].set_value(float(Property.value));
            if Property.name == "criteria":
                if Property.value == "pos":
                    self.widgets['Pos'].set_active(True);
                elif Property.value == "val":
                    self.widgets['Val'].set_active(True);
            if Property.name == "minORmax":
                if Property.value == "min":
                    self.widgets['min'].set_active(True);
                elif Property.value == "max":
                    self.widgets['max'].set_active(True);

        self.configure()

        # load help text
        t_oS2iHelp = XMLParser(self.m_sDataDir + "help/minMax" + _("_en.help"))

        t_oTextBuffer = gtk.TextBuffer()

        t_oTextBuffer.set_text(unicode(str(t_oS2iHelp.getTag("help").getTag("content").getTagContent())))

        self.widgets['HelpView'].set_buffer(t_oTextBuffer)

    # ----------------------------------------------------------------------

    def __del__(self):
        pass

    # ----------------------------------------------------------------------

    def on_prop_confirm_clicked(self, *args):

        for Property in self.block_properties:
            if Property.name == "minX":
                Property.value = unicode(self.widgets['minX'].get_value())
            if Property.name == "maxX":
                Property.value = unicode(self.widgets['maxX'].get_value())
            if Property.name == "minY":
                Property.value = unicode(self.widgets['minY'].get_value())
            if Property.name == "maxY":
                Property.value = unicode(self.widgets['maxY'].get_value())
            if Property.name == "minVal":
                Property.value = unicode(self.widgets['minVal'].get_value())
            if Property.name == "maxVal":
                Property.value = unicode(self.widgets['maxVal'].get_value())
            if Property.name == "criteria":
                if self.widgets['Pos'].get_active():
                    Property.value = u"pos"
                elif self.widgets['Val'].get_active():
                    Property.value = u"val"
            if Property.name == "minORmax":
                if self.widgets['min'].get_active():
                    Property.value = u"min"
                else:
                    Property.value = u"max"

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
    for propIter in self.properties:
        if propIter[0] == 'minX':
            minX = propIter[1]
        elif propIter[0] == 'maxX':
            maxX = propIter[1]
        elif propIter[0] == 'minY':
            minY = propIter[1]
        elif propIter[0] == 'maxY':
            maxY = propIter[1]
        elif propIter[0] == 'minVal':
            minVal = propIter[1]
        elif propIter[0] == 'maxVal':
            maxVal = propIter[1]
        elif propIter[0] == 'minORmax':
            minORmax = propIter[1]
        elif propIter[0] == 'criteria':
            checkCrit = propIter[1]
    self.imagesIO = \
        'IplImage * block' + self.blockNumber + '_img_i1 = NULL;\n' + \
        'double block' + self.blockNumber + '_double_o1;\n' + \
        'CvPoint block' + self.blockNumber + '_point_o2 = cvPoint(0,0);\n'
    self.functionCall = '\nif(block' + self.blockNumber + '_img_i1)\n{\n' + \
                        '	double minVal,maxVal;\n' + \
                        '	CvPoint minP,maxP;\n' + \
                        '	block' + self.blockNumber + '_double_o1 = 0;\n' + \
                        '	cvMinMaxLoc(block' + self.blockNumber + '_img_i1, &minVal, &maxVal, &minP, &maxP, NULL);\n'
    if minORmax == 'max':
        self.functionCall += '	minP = maxP;\n	minVal = maxVal;\n'

    self.functionCall += '	block' + self.blockNumber + '_point_o2 = minP;\n'

    if checkCrit == "pos":
        self.functionCall += '	if(minP.x >= ' + minX + ' && minP.x <= ' + maxX + ')\n' + \
                             '		if(minP.y >= ' + minY + ' && minP.y <= ' + maxY + ')\n' + \
                             '			block' + self.blockNumber + '_double_o1 = 1.0;\n'
    elif checkCrit == "val":
        self.functionCall += '	if(minVal >= ' + minVal + ' && minVal <= ' + maxVal + ')\n' + \
                             '		block' + self.blockNumber + '_double_o1 = 1.0;\n'
    self.functionCall += '}\n'
    self.dealloc = 'cvReleaseImage(&block' + self.blockNumber + '_img_i1);\n'


# ------------------------------------------------------------------------------
# Block Setup
# ------------------------------------------------------------------------------
def getBlock():
    return {"Label": _("Find Min or Max"),
            "Path": {"Python": "minMax",
                     "Glade": "glade/minMax.ui",
                     "Xml": "xml/minMax.xml"},
            "Inputs": 1,
            "Outputs": 2,
            "Icon": "images/minMax.png",
            "Color": "50:50:200:150",
            "InTypes": {0: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_DOUBLE", 1: "HRP_POINT"},
            "Description": _("Finds min or max from input image and judges it according to a custom criteria."),
            "TreeGroup": _("Feature Detection")
            }
