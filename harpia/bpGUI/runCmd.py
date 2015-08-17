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

        filename = self.m_sDataDir + 'glade/runCmd.ui'
        self.m_oPropertiesXML = PropertiesXML
        self.m_oS2iBlockProperties = S2iBlockProperties

        widget_list = [
            'Properties',
            'cmdString',
            'BackgroundColor',
            'BorderColor',
            'HelpView',
            'enIsntZero'
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
            if Property.name == "cmdString":
                self.widgets['cmdString'].set_text(Property.value)
            if Property.name == "enIsntZero":
                self.widgets['enIsntZero'].set_active(Property.value == "True")

        self.configure()

        # load help text
        t_oS2iHelp = XMLParser(self.m_sDataDir + "help/runCmd" + _("_en.help"))

        t_oTextBuffer = gtk.TextBuffer()

        t_oTextBuffer.set_text(unicode(str(t_oS2iHelp.getTag("help").getTag("content").getTagContent())))

        self.widgets['HelpView'].set_buffer(t_oTextBuffer)

    # ----------------------------------------------------------------------

    def __del__(self):
        pass

    # ----------------------------------------------------------------------

    def on_prop_confirm_clicked(self, *args):
        for Property in self.block_properties:
            if Property.name == "cmdString":
                Property.value = unicode(self.widgets['cmdString'].get_text())
            if Property.name == "enIsntZero":
                Property.value = unicode(self.widgets['enIsntZero'].get_active())

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
    cmdString = 'echo no properties'
    enIsntZero = False
    for propIter in blockTemplate.properties:
        if propIter[0] == 'cmdString':
            cmdString = propIter[1]
        if propIter[0] == 'enIsntZero':
            enIsntZero = (propIter[1] == "True")
    cmdString = cmdString.replace(r"'", r"\'")
    cmdString = cmdString.replace(r'"', r'\"')
    blockTemplate.imagesIO = \
        'double block' + blockTemplate.blockNumber + '_double_i1;\n' + \
        'double block' + blockTemplate.blockNumber + '_double_o1;\n'
    blockTemplate.functionCall = '\nif('
    if enIsntZero:
        blockTemplate.functionCall += 'block' + blockTemplate.blockNumber + '_double_i1 > 0.0){\n'
    else:
        blockTemplate.functionCall += '1){\n'
    blockTemplate.functionCall += 'char outPutStr[' + str(len(cmdString) + 30) + '];\n' + \
                                  'snprintf(outPutStr,' + str(len(
        cmdString) + 30) + ',"export HRP_DB=%f;' + cmdString + '",(float)block' + blockTemplate.blockNumber + '_double_i1);' + \
                                  'system(outPutStr);}\n' + \
                                  'block' + blockTemplate.blockNumber + '_double_o1 = block' + blockTemplate.blockNumber + '_double_i1;\n'
    blockTemplate.dealloc = '//nothing to deallocate\n'


# ------------------------------------------------------------------------------
# Block Setup
# ------------------------------------------------------------------------------
def getBlock():
    return {"Label": _("Run Command"),
            "Path": {"Python": "runCmd",
                     "Glade": "glade/runCmd.ui",
                     "Xml": "xml/runCmd.xml"},
            "Inputs": 1,
            "Outputs": 1,
            "Icon": "images/runCmd.png",
            "Color": "200:200:60:150",
            "InTypes": {0: "HRP_DOUBLE"},
            "OutTypes": {0: "HRP_DOUBLE"},
            "Description": _("Runs a shell command depending on the input value."),
            "TreeGroup": _("Experimental")
            }
