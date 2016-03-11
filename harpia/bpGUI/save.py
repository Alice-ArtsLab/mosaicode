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

        filename = self.m_sDataDir + 'glade/save.ui'
        self.m_oPropertiesXML = PropertiesXML
        self.m_oS2iBlockProperties = S2iBlockProperties

        widget_list = [
            'Properties',
            'SAVEFilename',
            'SAVEType',
            'BackgroundColor',
            'BorderColor',
            'HelpView'
        ]

        handlers = [
            'on_SAVEButtonSearch_clicked',
            'on_BackColorButton_clicked',
            'on_BorderColorButton_clicked',
            'on_cancel_clicked',
            'on_save_confirm_clicked'
        ]

        top_window = 'Properties'

        GladeWindow.__init__(self, filename, top_window, widget_list, handlers)

        # load properties values
        self.block_properties = self.m_oPropertiesXML.getTag("properties").getTag("block").getChildTags("property")
        for Property in self.block_properties:

            if Property.name == "filename":
                self.widgets['SAVEFilename'].set_text(Property.value);
                #           if Property.name == "filetype":
                #               if Property.value == "png":
                #                   self.widgets['SAVEType'].set_active( int(0) )
                #               if Property.value == "jpeg":
                #                   self.widgets['SAVEType'].set_active( int(1) )

        self.configure()

        # load help text
        # t_oS2iHelp = XMLParser(self.m_sDataDir + "help/save" + _("_en.help"))

        # t_oTextBuffer = gtk.TextBuffer()

        # t_oTextBuffer.set_text(unicode(str(t_oS2iHelp.getTag("help").getTag("content").getTagContent())))

        # self.widgets['HelpView'].set_buffer(t_oTextBuffer)

    #----------------Help Text--------------------------------------

    def getHelp(self):#adicionado help
        return "Salva uma imagem em uma mídia indicada pelo usuário.\
        Atualmente a imagem é salva como PNG por padrão." 


    # ----------------------------------------------------------------------

    def __del__(self):

        pass

    # ----------------------------------------------------------------------

    def on_save_confirm_clicked(self, *args):

        for Property in self.block_properties:

            if Property.name == "filename":
                Property.value = unicode(self.widgets['SAVEFilename'].get_text())

            #            if Property.name == "filetype":
            #
            #               t_nActive = self.widgets['SAVEType'].get_active( )
            #
            #                if int(t_nActive) == 0:
            #                    Property.value = unicode("png")
            #                if int(t_nActive) == 1:
            #                    Property.value = unicode("jpeg")

        self.m_oS2iBlockProperties.SetPropertiesXML(self.m_oPropertiesXML)

        self.m_oS2iBlockProperties.SetBorderColor(self.m_oBorderColor)

        self.m_oS2iBlockProperties.SetBackColor(self.m_oBackColor)

        self.widgets['Properties'].destroy()

    # ----------------------------------------------------------------------

    def on_SAVEButtonSearch_clicked(self, *args):

        dialog = gtk.FileChooserDialog("Salvar...",
                                       None,
                                       gtk.FILE_CHOOSER_ACTION_SAVE,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_SAVE, gtk.RESPONSE_OK))

        dialog.set_default_response(gtk.RESPONSE_OK)

        if os.name == 'posix':
            dialog.set_current_folder(os.path.expanduser("~"))

        filter = gtk.FileFilter()
        filter.set_name("Todos os arquivos")
        filter.add_pattern("*")
        dialog.add_filter(filter)

        filter = gtk.FileFilter()
        filter.set_name("imagens")
        filter.add_mime_type("*.jpg")
        dialog.add_filter(filter)

        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            response = dialog.get_filename()
        elif response == gtk.RESPONSE_CANCEL:
            response = None
        dialog.destroy()

        self.widgets['SAVEFilename'].set_text(response);

        # ----------------------------------------------------------------------


# SaveProperties = Properties()
# SaveProperties.show( center=0 )

# ------------------------------------------------------------------------------
# Code generation
# ------------------------------------------------------------------------------
def generate(blockTemplate):
    for propIter in blockTemplate.properties:
        if propIter[0] == 'filename':
            saveFilename = os.path.expanduser(propIter[1])
    blockTemplate.imagesIO = \
        'IplImage * block' + blockTemplate.blockNumber + '_img_i1 = NULL;\n' + \
        'IplImage * block' + blockTemplate.blockNumber + '_img_o1 = NULL;\n'
    blockTemplate.functionCall = \
        'block' + blockTemplate.blockNumber + '_img_o1 = cvCloneImage(block' + blockTemplate.blockNumber + '_img_i1);\n' + \
        '\nif(block' + blockTemplate.blockNumber + '_img_i1)\n' + \
        'cvSaveImage("' + saveFilename + '" ,block' + blockTemplate.blockNumber + '_img_i1);\n'
    blockTemplate.dealloc = 'cvReleaseImage(&block' + blockTemplate.blockNumber + '_img_o1);\n' + \
                            'cvReleaseImage(&block' + blockTemplate.blockNumber + '_img_i1);\n'


# ------------------------------------------------------------------------------
# Block Setup
# ------------------------------------------------------------------------------
def getBlock():
    return {"Label": _("Save Image"),
            "Path": {"Python": "save",
                     "Glade": "glade/save.ui",
                     "Xml": "xml/save.xml"},
            "Icon": "images/save.png",
            "Color": "50:100:200:150",
            "InTypes": {0: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "Description": _("Save image on a file indicated by the user."),
            "TreeGroup": _("General")
            }
