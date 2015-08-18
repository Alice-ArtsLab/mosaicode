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

        filename = self.m_sDataDir + 'glade/getSize.ui'
        self.m_oPropertiesXML = PropertiesXML
        self.m_oS2iBlockProperties = S2iBlockProperties

        widget_list = [
            'Properties',
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

        self.configure()

        # load help text
        t_oS2iHelp = XMLParser(self.m_sDataDir + "help/getSize" + _("_en.help"))

        t_oTextBuffer = gtk.TextBuffer()

        t_oTextBuffer.set_text(unicode(str(t_oS2iHelp.getTag("help").getTag("content").getTagContent())))

        self.widgets['HelpView'].set_buffer(t_oTextBuffer)

    # ----------------------------------------------------------------------

    def __del__(self):
        pass

    # ----------------------------------------------------------------------

    def on_prop_confirm_clicked(self, *args):
        # for Property in self.m_oPropertiesXML.properties.block.property:
        # if Property.name == "method":
        # Active = self.widgets['method'].get_active( )
        # if int(Active) == 0:
        # Property.value = unicode("CV_INTER_NN")
        # if int(Active) == 1:
        # Property.value = unicode("CV_INTER_LINEAR")
        # if int(Active) == 2:
        # Property.value = unicode("CV_INTER_AREA")
        # if int(Active) == 3:
        # Property.value = unicode("CV_INTER_CUBIC")

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
    # if propIter[0] == 'type':
    # delayType = propIter[1]
    # elif propIter[0] == 'frameNumber':
    # frameNumber = int(float(propIter[1]))
    # frameNumber = max(frameNumber,1)
    blockTemplate.imagesIO = 'IplImage * block' + blockTemplate.blockNumber + '_img_i1 = NULL;\n' + \
                             'CvRect block' + blockTemplate.blockNumber + '_rect_o1 = cvRect( 0, 0, 1, 1);\n'

    blockTemplate.functionCall = '\nif(block' + blockTemplate.blockNumber + '_img_i1)\n{\n' + \
                                 '	block' + blockTemplate.blockNumber + '_rect_o1 = cvRect( 0, 0, block' + blockTemplate.blockNumber + '_img_i1->width, block' + blockTemplate.blockNumber + '_img_i1->height);\n' + \
                                 '}\n'
    blockTemplate.dealloc = 'cvReleaseImage(&block' + blockTemplate.blockNumber + '_img_i1);\n'


# ------------------------------------------------------------------------------
# Block Setup
# ------------------------------------------------------------------------------
def getBlock():
    return {'Label': _('Get Size'),
            'Path': {'Python': 'getSize',
                     'Glade': 'glade/getSize.ui',
                     'Xml': 'xml/getSize.xml'},
            'Inputs': 1,
            'Outputs': 1,
            'Icon': 'images/getSize.xpm',
            'Color': '250:20:30:150',
            'InTypes': {0: 'HRP_IMAGE'},
            'OutTypes': {0: 'HRP_RECT'},
            'Description': _('Extracts the input image size'),
            'TreeGroup': _('Experimental'),
            'TimeShifts': False
            }
