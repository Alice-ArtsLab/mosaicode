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

        filename = self.m_sDataDir + 'glade/isOnRect.ui'
        self.m_oPropertiesXML = PropertiesXML
        self.m_oS2iBlockProperties = S2iBlockProperties

        widget_list = [
            'Properties',
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
        # for Property in self.m_oPropertiesXML.properties.block.property:
        # if Property.name == "angle":
        # self.widgets['angle'].set_value( float(Property.value) );


        self.configure()

        # load help text
        # t_oS2iHelp = XMLParser(self.m_sDataDir + 'help/isOnRect' + _('_en.help'))

        # t_oTextBuffer = gtk.TextBuffer()

        # t_oTextBuffer.set_text(unicode(str(t_oS2iHelp.getTag("help").getTag("content").getTagContent())))

        # self.widgets['HelpView'].set_buffer(t_oTextBuffer)

    # ----------------------------------------------------------------------
    def getHelp(self):
        return "Detecta formas circulares na imagem de entrada.\
         Saida 1 é a resposta da avaliacao(*) e a saida dois mostra os circulos encontrados."

    #----------------------------------------------------------------------








    def __del__(self):
        pass

    # ----------------------------------------------------------------------

    def on_prop_confirm_clicked(self, *args):
        self.widgets['prop_confirm'].grab_focus()
        # for Property in self.m_oPropertiesXML.properties.block.property:
        # if Property.name == "angle":
        # Property.value = unicode(self.widgets['angle'].get_value())


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
    # for propIter in blockTemplate.properties:
    # if propIter[0] == 'method':
    # interMethod = propIter[1]

    blockTemplate.imagesIO = 'CvRect block$$_rect_i2;\n' + \
                             'CvPoint block$$_point_i1;\n' + \
                             'double block$$_double_o1;\n'
    blockTemplate.functionCall = '\n block$$_double_o1 = 0.0;\n' + \
                                 'if(block$$_point_i1.x >= block$$_rect_i2.x)\n' + \
                                 '	if(block$$_point_i1.y >= block$$_rect_i2.y)\n' + \
                                 '		if(block$$_point_i1.x < block$$_rect_i2.x + block$$_rect_i2.width)\n' + \
                                 '			if(block$$_point_i1.y < block$$_rect_i2.y + block$$_rect_i2.height)\n' + \
                                 '				block$$_double_o1 = 1.0;\n'
    blockTemplate.dealloc = ''


# ------------------------------------------------------------------------------
# Block Setup
# ------------------------------------------------------------------------------
def getBlock():
    return {'Label': _('Check Point'),
            'Path': {'Python': 'isOnRect',
                     'Glade': 'glade/isOnRect.ui',
                     'Xml': 'xml/isOnRect.xml'},
            'Icon': 'images/isOnRect.png',
            'Color': '50:50:200:150',
            'InTypes': {0: 'HRP_POINT', 1: 'HRP_RECT'},
            'OutTypes': {0: 'HRP_DOUBLE'},
            'Description': _('Checks Wheather the given point is inside the given rectangle'),
            'TreeGroup': _('Experimental')
            }
