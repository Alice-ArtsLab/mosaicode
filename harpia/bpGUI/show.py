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

        filename = self.m_sDataDir + 'glade/show.ui'
        self.m_oPropertiesXML = PropertiesXML
        self.m_oS2iBlockProperties = S2iBlockProperties

        widget_list = [
            'Properties',
            'SHOWDisable',
            'BackgroundColor',
            'BorderColor',
            'HelpView'
        ]

        handlers = [
            'on_BackColorButton_clicked',
            'on_BorderColorButton_clicked',
            'on_cancel_clicked',
            'on_confirm_clicked'
        ]

        top_window = 'Properties'

        GladeWindow.__init__(self, filename, top_window, widget_list, handlers)


        # load properties values
        # There is no properties

        # load block state
        t_bState = self.m_oS2iBlockProperties.GetState()

        self.widgets['SHOWDisable'].set_active(not t_bState)

        self.configure()


        # load help text
        # t_oS2iHelp = XMLParser(self.m_sDataDir + "help/show" + _("_en.help"))

        # t_oTextBuffer = gtk.TextBuffer()

        # t_oTextBuffer.set_text(unicode(str(t_oS2iHelp.getTag("help").getTag("content").getTagContent())))

        # self.widgets['HelpView'].set_buffer(t_oTextBuffer)

    #----------------Help Text--------------------------------------

    def getHelp(self):#adicionado help
        return "Mostra uma imagem da cadeia de processamento de imagens."

    # ----------------------------------------------------------------------

    def __del__(self):
        pass


# ShowProperties = Properties()
# ShowProperties.show( center=0 )

# ------------------------------------------------------------------------------
# Code generation
# ------------------------------------------------------------------------------
def generate(blockTemplate):
    import harpia.gerador
    harpia.gerador.g_ShowCount += 1
    blockTemplate.imagesIO = \
        'IplImage * block$$_img_i1 = NULL;\n' + \
        'IplImage * block$$_img_o1 = NULL;\n'
    if (not harpia.gerador.g_bLive):
        blockTemplate.functionCall = '\nif(block$$_img_i1){\n' + \
                                     ' block$$_img_o1 = cvCloneImage(block$$_img_i1);\n' + \
                                     'cvSaveImage("block$$_OUT.png" ,block$$_img_i1);}\n'
    else:
        blockTemplate.functionCall = '\nif(block$$_img_i1){\n' + \
                                     ' block$$_img_o1 = cvCloneImage(block$$_img_i1);\n' + \
                                     'cvNamedWindow("block$$_img_o1",CV_WINDOW_AUTOSIZE );\n cvShowImage("block$$_img_o1",block$$_img_i1);} \n'
    blockTemplate.dealloc = 'cvReleaseImage(&block$$_img_o1);\n' + \
                            'cvReleaseImage(&block$$_img_i1);\n'


# ------------------------------------------------------------------------------
# Block Setup
# ------------------------------------------------------------------------------
def getBlock():
    return {"Label": _("Show Image"),
            "Path": {"Python": "show",
                     "Glade": "glade/show.ui",
                     "Xml": "xml/show.xml"},
            "Icon": "images/show.png",
            "Color": "50:100:200:150",
            "InTypes": {0: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "Description": _("Shows the input image on a new window."),
            "TreeGroup": _("General")
            }
            
def getXML():
    return r"""<properties>
      <block type='02' id=''>
	<property name='state' value='true' />
      </block>
</properties>"""
