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
import gettext
from harpia.utils.XMLUtils import XMLParser

_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)


# ----------------------------------------------------------------------

class Properties(GladeWindow, S2iCommonProperties):
    # ----------------------------------------------------------------------

    def __init__(self, PropertiesXML, S2iBlockProperties):
        self.m_sDataDir = os.environ['HARPIA_DATA_DIR']

        filename = self.m_sDataDir + 'glade/xor.ui'
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
            'on_confirm_clicked',
            'on_BackColorButton_clicked',
            'on_BorderColorButton_clicked'
        ]

        top_window = 'Properties'
        GladeWindow.__init__(self, filename, top_window, widget_list, handlers)
        self.configure()

    #----------------Help Text--------------------------------------

    def getHelp(self):#adicionado help
        return "Realiza a operação lógica XOR entre duas imagens."

    # ----------------------------------------------------------------------

    def __del__(self):
        pass

        # ----------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Code generation
# ------------------------------------------------------------------------------
def generate(blockTemplate):
    import opencvcommon
    blockTemplate.header += opencvcommon.adjust_images_size()

    blockTemplate.imagesIO = \
        'IplImage * block$$_img_i1 = NULL;\n' + \
        'IplImage * block$$_img_i2 = NULL;\n' + \
        'IplImage * block$$_img_o1 = NULL;\n'
    blockTemplate.functionCall = '\nif(block$$_img_i1){\n' + \
                                 'block$$_img_o1 = cvCreateImage(cvSize(block$$' + \
                                 '_img_i1->width,block$$_img_i1->height),block$$' + \
                                 '_img_i1->depth,block$$_img_i1->nChannels);\n' + \
                                 'adjust_images_size(block$$_img_i1, block$$_img_i2, block$$_img_o1);\n' + \
                                  'cvXor(block$$_img_i1, block$$_img_i2, block$$' + \
                                 '_img_o1,0);\ncvResetImageROI(block$$_img_o1);}\n'
    blockTemplate.dealloc = 'cvReleaseImage(&block$$_img_o1);\n' + \
                            'cvReleaseImage(&block$$_img_i1);\n' + \
                            'cvReleaseImage(&block$$_img_i2);\n'


# ------------------------------------------------------------------------------
# Block Setup
# ------------------------------------------------------------------------------
def getBlock():
    return {"Label": _("Xor"),
            "Path": {"Python": "xor",
                     "Glade": "glade/xor.ui",
                     "Xml": "xml/xor.xml"},
            "Icon": "images/xor.png",
            "Color": "10:180:10:150",
            "InTypes": {0: "HRP_IMAGE", 1: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "Description": _("Logical XOR (exclusive-or) operation between two images."),
            "TreeGroup": _("Arithmetic and logical operations")
            }
