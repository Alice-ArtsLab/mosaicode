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

        filename = self.m_sDataDir + 'glade/newRect.ui'
        self.m_oPropertiesXML = PropertiesXML
        self.m_oS2iBlockProperties = S2iBlockProperties

        widget_list = [
            'Properties',
            'x0',
            'y0',
            'width',
            'height',
            'BackgroundColor',
            'BorderColor',
            'HelpView',
            'prop_confirm'
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
            if Property.name == "x0":
                self.widgets['x0'].set_value(float(Property.value));
            if Property.name == "y0":
                self.widgets['y0'].set_value(float(Property.value));
            if Property.name == "width":
                self.widgets['width'].set_value(float(Property.value));
            if Property.name == "height":
                self.widgets['height'].set_value(float(Property.value));

        self.configure()

        # load help text
        # t_oS2iHelp = XMLParser(self.m_sDataDir + 'help/newRect' + _('_en.help'))

        # t_oTextBuffer = gtk.TextBuffer()

        # t_oTextBuffer.set_text(unicode(str(t_oS2iHelp.getTag("help").getTag("content").getTagContent())))

        # self.widgets['HelpView'].set_buffer(t_oTextBuffer)

    # ----------------------------------------------------------------------
    def getHelp(self):
        return "Detecta formas circulares na imagem de entrada.\
        Saida 1 é a resposta da avaliacao(*) e a saida dois mostra os circulos encontrados."

    # ----------------------------------------------------------------------


    def __del__(self):
        pass

    # ----------------------------------------------------------------------

    def on_prop_confirm_clicked(self, *args):

        self.widgets['prop_confirm'].grab_focus()

        for Property in self.block_properties:
            if Property.name == "x0":
                Property.value = unicode(self.widgets['x0'].get_value())
            if Property.name == "y0":
                Property.value = unicode(self.widgets['y0'].get_value())
            if Property.name == "width":
                Property.value = unicode(self.widgets['width'].get_value())
            if Property.name == "height":
                Property.value = unicode(self.widgets['height'].get_value())

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
        if propIter[0] == 'x0':
            x0 = propIter[1]
        elif propIter[0] == 'y0':
            y0 = propIter[1]
        elif propIter[0] == 'width':
            rctWidth = propIter[1]
        elif propIter[0] == 'height':
            rctHeight = propIter[1]
    blockTemplate.imagesIO = '\nCvRect block$$_rect_o1;\n'
    blockTemplate.functionCall = 'block$$_rect_o1 = cvRect(' + str(
        int(float(x0))) + ', ' + str(int(float(y0))) + ', ' + str(int(float(rctWidth))) + ', ' + str(
        int(float(rctHeight))) + ');'
    blockTemplate.dealloc = ''


# ------------------------------------------------------------------------------
# Block Setup
# ------------------------------------------------------------------------------
def getBlock():
    return {'Label': _('New Rectangle'),
            'Path': {'Python': 'newRect',
                     'Glade': 'glade/newRect.ui',
                     'Xml': 'xml/newRect.xml'},
            'Icon': 'images/newRect.png',
            'Color': '50:50:200:150',
            'InTypes': "",
            'OutTypes': {0: 'HRP_RECT'},
            'Description': _('Creates new rectangle'),
            'TreeGroup': _('Basic Data Type'),
            "IsSource": True
            }
