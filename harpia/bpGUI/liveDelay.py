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

        filename = self.m_sDataDir + 'glade/liveDelay.ui'
        self.m_oPropertiesXML = PropertiesXML
        self.m_oS2iBlockProperties = S2iBlockProperties

        widget_list = [
            'Properties',
            'frameNumber',
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
        for Property in self.block_properties:
            name = Property.getAttr("name")
            value = Property.getAttr("value")

            if name == "frameNumber":
                self.widgets['frameNumber'].set_value(int(float(value)))

        self.configure()

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

            if Property.name == "frameNumber":
                print Property.value
                Property.value = unicode(str(int(self.widgets['frameNumber'].get_value())))
                print Property.value

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
        if propIter[0] == 'type':
            delayType = propIter[1]
        elif propIter[0] == 'frameNumber':
            frameNumber = int(float(propIter[1]))
            frameNumber = max(frameNumber, 1)
    blockTemplate.imagesIO = 'IplImage * block$$_img_i1 = NULL;\n' + \
                             'IplImage * block$$_img_o1 = NULL;\n' + \
                             'int block$$_t_idx = 0;\n' + \
                             'IplImage * block$$_buffer[' + str(frameNumber) + '] = {'
    for idx in range(frameNumber):
        blockTemplate.imagesIO += 'NULL'
        if idx <> frameNumber - 1:
            blockTemplate.imagesIO += ','
    blockTemplate.imagesIO += '};\n'

    for idx in range(frameNumber):
        blockTemplate.imagesIO += 'block$$_buffer[' + str(
            idx) + '] = cvCreateImage( cvSize(640,480), 8, 3);\n'
        blockTemplate.imagesIO += 'cvSetZero(block$$_buffer[' + str(idx) + ']);\n'
    blockTemplate.imagesIO += 'block$$_img_o1 = block$$_buffer[' + str(
        frameNumber - 1) + '];\n'

    blockTemplate.functionCall = '\nif(block$$_img_i1)\n{\n' + \
                                 '	cvReleaseImage(&(block$$_buffer[block$$_t_idx]));\n' + \
                                 '	block$$_buffer[block$$_t_idx] = cvCloneImage(block$$_img_i1);\n' + \
                                 '	block$$_t_idx++;\n' + \
                                 '	block$$_t_idx %= ' + str(frameNumber) + ';\n' + \
                                 '	block$$_img_o1 = block$$_buffer[block$$_t_idx];\n' + \
                                 '}\n'
    blockTemplate.dealloc = 'cvReleaseImage(&block$$_img_i1);\n'
    blockTemplate.outDealloc = 'for(block$$_t_idx=0;block$$_t_idx<' + str(
        frameNumber) + ';block$$_t_idx++)\n' + \
                               '	if(block$$_buffer[block$$_t_idx] != NULL)\n' + \
                               '		cvReleaseImage(&(block$$_buffer[block$$_t_idx]));\n'


# ------------------------------------------------------------------------------
# Block Setup
# ------------------------------------------------------------------------------
def getBlock():
    return {'Label': _('Live Delay'),
            'Path': {'Python': 'liveDelay',
                     'Glade': 'glade/liveDelay.ui',
                     'Xml': 'xml/liveDelay.xml'},
            'Icon': 'images/liveDelay.png',
            'Color': '250:20:30:150',
            'InTypes': {0: 'HRP_IMAGE'},
            'OutTypes': {0: 'HRP_IMAGE'},
            'Description': _('Inserts a delay inside a live stream'),
            'TreeGroup': _('General'),
            'TimeShifts': True
            }
