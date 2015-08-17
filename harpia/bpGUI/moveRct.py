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

        filename = self.m_sDataDir + 'glade/moveRct.ui'
        self.m_oPropertiesXML = PropertiesXML
        self.m_oS2iBlockProperties = S2iBlockProperties

        widget_list = [
            'Properties',
            'offset_x',
            'offset_y',
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

        self.block_properties = self.m_oPropertiesXML.getTag("properties").getTag("block").getChildTags("property")
        # load properties values
        for Property in self.block_properties:
            if Property.name == "offset_x":
                self.widgets['offset_x'].set_value(float(Property.value));
            if Property.name == "offset_y":
                self.widgets['offset_y'].set_value(float(Property.value));

        self.configure()

        # load help text
        t_oS2iHelp = XMLParser(self.m_sDataDir + 'help/moveRct' + _('_en.help'))

        t_oTextBuffer = gtk.TextBuffer()

        t_oTextBuffer.set_text(unicode(str(t_oS2iHelp.getTag("help").getTag("content").getTagContent())))

        self.widgets['HelpView'].set_buffer(t_oTextBuffer)

    # ----------------------------------------------------------------------

    def __del__(self):
        pass

    # ----------------------------------------------------------------------

    def on_prop_confirm_clicked(self, *args):

        self.widgets['prop_confirm'].grab_focus()

        self.m_oS2iBlockProperties.SetPropertiesXML(self.m_oPropertiesXML)

        for Property in self.block_properties:
            if Property.name == "offset_x":
                Property.value = unicode(self.widgets['offset_x'].get_value())
            if Property.name == "offset_y":
                Property.value = unicode(self.widgets['offset_y'].get_value())

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
        if propIter[0] == 'offset_x':
            offset_x = propIter[1]
        if propIter[0] == 'offset_y':
            offset_y = propIter[1]
    blockTemplate.imagesIO = 'CvRect block' + blockTemplate.blockNumber + '_rect_i1;\n' + \
                             'CvPoint block' + blockTemplate.blockNumber + '_point_i2;\n' + \
                             'CvRect block' + blockTemplate.blockNumber + '_rect_o1;\n'
    blockTemplate.functionCall = 'block' + blockTemplate.blockNumber + '_rect_o1 = block' + blockTemplate.blockNumber + '_rect_i1;\n' + \
                                 'block' + blockTemplate.blockNumber + '_rect_o1.x = block' + blockTemplate.blockNumber + '_point_i2.x + ' + offset_x + ';\n' + \
                                 'block' + blockTemplate.blockNumber + '_rect_o1.y = block' + blockTemplate.blockNumber + '_point_i2.y + ' + offset_y + ';\n'
    blockTemplate.dealloc = ''


# ------------------------------------------------------------------------------
# Block Setup
# ------------------------------------------------------------------------------
def getBlock():
    return {'Label': _('Move Rectangle'),
            'Path': {'Python': 'moveRct',
                     'Glade': 'glade/moveRct.ui',
                     'Xml': 'xml/moveRct.xml'},
            'Inputs': 2,
            'Outputs': 1,
            'Icon': 'images/moveRct.png',
            'Color': '50:50:200:150',
            'InTypes': {0: 'HRP_RECT', 1: 'HRP_POINT'},
            'OutTypes': {0: 'HRP_RECT'},
            'Description': _('Move Rectangle`s (0,0) point to input point'),
            'TreeGroup': _('Experimental')
            }
