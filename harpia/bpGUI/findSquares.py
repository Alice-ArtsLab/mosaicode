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

        filename = self.m_sDataDir + 'glade/findSquares.ui'
        self.m_oPropertiesXML = PropertiesXML
        self.m_oS2iBlockProperties = S2iBlockProperties

        widget_list = [
            'Properties',
            'BackgroundColor',
            'BorderColor',
            'HelpView',
            'minVal',
            'maxVal',
            'enMin',
            'enMax',
            'prop_confirm'
        ]

        handlers = [
            'on_cancel_clicked',
            'on_prop_confirm_clicked',
            'on_BackColorButton_clicked',
            'on_BorderColorButton_clicked',
            'on_enMin_toggled',
            'on_enMax_toggled'
        ]

        top_window = 'Properties'

        GladeWindow.__init__(self, filename, top_window, widget_list, handlers)

        self.block_properties = self.m_oPropertiesXML.getTag("properties").getTag("block").getChildTags("property")

        for Property in self.block_properties:

            name = Property.getAttr("name")
            value = Property.getAttr("value")

            if name == "minVal":
                self.widgets['minVal'].set_value(int(float(value)))
            if name == "maxVal":
                self.widgets['maxVal'].set_value(int(float(value)))
            if name == "enMin":
                self.widgets['enMin'].set_active(value == 'True')
            if name == "enMax":
                self.widgets['enMax'].set_active(value == 'True')

        self.configure()

        # load help text
        t_oS2iHelp = XMLParser(self.m_sDataDir + 'help/findSquares' + _('_en.help'))

        t_oTextBuffer = gtk.TextBuffer()

        t_oTextBuffer.set_text(unicode(str(t_oS2iHelp.getTag("help").getTag("content").getTagContent())))

        self.widgets['HelpView'].set_buffer(t_oTextBuffer)

    # ----------------------------------------------------------------------

    def __del__(self):
        pass

    # ----------------------------------------------------------------------

    def on_enMin_toggled(self, src):
        self.widgets['minVal'].set_sensitive(src.get_active())

    def on_enMax_toggled(self, src):
        self.widgets['maxVal'].set_sensitive(src.get_active())

    # ----------------------------------------------------------------------

    def on_prop_confirm_clicked(self, *args):
        self.widgets['prop_confirm'].grab_focus()

        for Property in self.block_properties:

            name = Property.getAttr("name")

            if name == "minVal":
                Property.setAttr("value", unicode(str(int(self.widgets['minVal'].get_value()))))
            if name == "maxVal":
                Property.setAttr("value", unicode(str(int(self.widgets['maxVal'].get_value()))))
            if name == "enMin":
                Property.setAttr("value", unicode(str(self.widgets['enMin'].get_active())))
            if name == "enMax":
                Property.setAttr("value", unicode(str(self.widgets['enMax'].get_active())))

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
    global usesFindSquares
    usesFindSquares = 1
    for propIter in blockTemplate.properties:
        if propIter[0] == 'enMin':
            enMin = (propIter[1] == "True")
        if propIter[0] == 'enMax':
            enMax = (propIter[1] == "True")
        if propIter[0] == 'minVal':
            minVal = propIter[1]
        if propIter[0] == 'maxVal':
            maxVal = propIter[1]
    if not enMin:
        minVal = -1
    if not enMax:
        maxVal = -1
    blockTemplate.imagesIO = \
        'IplImage * block' + blockTemplate.blockNumber + '_img_i1 = NULL;\n' + \
        'IplImage * block' + blockTemplate.blockNumber + '_img_o2 = NULL;\n' + \
        'double block' + blockTemplate.blockNumber + '_double_o1;\n' + \
        'CvMemStorage * block' + blockTemplate.blockNumber + '_storage = NULL;\n'
    blockTemplate.functionCall = '\nif(block' + blockTemplate.blockNumber + '_img_i1){\n' + \
                                 '	block' + blockTemplate.blockNumber + '_img_o2 = cvCloneImage(block' + blockTemplate.blockNumber + '_img_i1);\n' + \
                                 '	block' + blockTemplate.blockNumber + '_storage = cvCreateMemStorage(0);\n' + \
                                 '	block' + blockTemplate.blockNumber + '_double_o1 = (double)drawSquares( block' + blockTemplate.blockNumber + '_img_o2, findSquares4( block' + blockTemplate.blockNumber + '_img_o2, block' + blockTemplate.blockNumber + '_storage , ' + str(
        minVal) + ', ' + str(maxVal) + ') );\n' + \
                                 '	cvClearMemStorage( block' + blockTemplate.blockNumber + '_storage );\n' + \
                                 '}\n'
    blockTemplate.dealloc = 'cvReleaseImage(&block' + blockTemplate.blockNumber + '_img_o2);\n' + \
                            'cvReleaseImage(&block' + blockTemplate.blockNumber + '_img_i1);\n' + \
                            'cvReleaseMemStorage(&block' + blockTemplate.blockNumber + '_storage );\n'


# ------------------------------------------------------------------------------
# Block Setup
# ------------------------------------------------------------------------------
def getBlock():
    return {'Label': _('Find Squares'),
            'Path': {'Python': 'findSquares',
                     'Glade': 'glade/findSquares.ui',
                     'Xml': 'xml/findSquares.xml'},
            'Inputs': 1,
            'Outputs': 2,
            'Icon': 'images/findSquares.png',
            'Color': '50:50:200:150',
            'InTypes': {0: 'HRP_IMAGE'},
            'OutTypes': {0: "HRP_DOUBLE", 1: "HRP_IMAGE"},
            'Description': _(
                'Finds four-sided polygons on the input image.\n Output 1 = Number of detected Polygons\n Output 2 = The input image tagged with the found polygons.'),
            'TreeGroup': _('Feature Detection')
            }
