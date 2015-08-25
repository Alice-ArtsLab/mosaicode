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

        filename = self.m_sDataDir + 'glade/rotate.ui'
        self.m_oPropertiesXML = PropertiesXML
        self.m_oS2iBlockProperties = S2iBlockProperties

        widget_list = [
            'Properties',
            'isAtCenter',
            'isAtPoint',
            'isScalling',
            'isFilling',
            'xC',
            'yC',
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
            if Property.name == "xC":
                self.widgets['xC'].set_value(float(Property.value));
            if Property.name == "yC":
                self.widgets['yC'].set_value(float(Property.value));

            if Property.name == "isFilling":
                if Property.value == "true":
                    self.widgets['isFilling'].set_active(True);
                else:
                    self.widgets['isFilling'].set_active(False);

            if Property.name == "isScalling":
                if Property.value == "true":
                    self.widgets['isScalling'].set_active(True);
                else:
                    self.widgets['isScalling'].set_active(False);

            if Property.name == "isCenter":
                if Property.value == "true":
                    self.widgets['isAtCenter'].set_active(True);
                else:
                    self.widgets['isAtPoint'].set_active(True);

        self.configure()

        # load help text
        t_oS2iHelp = XMLParser(self.m_sDataDir + "help/rotate" + _("_en.help"))

        t_oTextBuffer = gtk.TextBuffer()

        t_oTextBuffer.set_text(unicode(str(t_oS2iHelp.getTag("help").getTag("content").getTagContent())))

        self.widgets['HelpView'].set_buffer(t_oTextBuffer)

    # ----------------------------------------------------------------------

    def __del__(self):
        pass

    # ----------------------------------------------------------------------

    def on_prop_confirm_clicked(self, *args):

        self.widgets['prop_confirm'].grab_focus()

        for Property in self.block_properties:
            if Property.name == "xC":
                Property.value = unicode(self.widgets['xC'].get_value())
            if Property.name == "yC":
                Property.value = unicode(self.widgets['yC'].get_value())

            if Property.name == "isCenter":
                if self.widgets['isAtCenter'].get_active():
                    Property.value = u"true"
                else:
                    Property.value = u"false"

            if Property.name == "isFilling":
                if self.widgets['isFilling'].get_active():
                    Property.value = u"true"
                else:
                    Property.value = u"false"

            if Property.name == "isScalling":
                if self.widgets['isScalling'].get_active():
                    Property.value = u"true"
                else:
                    Property.value = u"false"

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
        if propIter[0] == 'xC':
            xC = propIter[1]
        elif propIter[0] == 'yC':
            yC = propIter[1]
        elif propIter[0] == 'isFilling':
            isFilling = propIter[1]
        elif propIter[0] == 'isCenter':
            isCenter = propIter[1]
        elif propIter[0] == 'isScalling':
            isScalling = propIter[1]

    blockTemplate.imagesIO = '\nIplImage * block' + blockTemplate.blockNumber + '_img_i1 = NULL;\n' + \
                             'double block' + blockTemplate.blockNumber + '_double_i2;\n' + \
                             'IplImage * block' + blockTemplate.blockNumber + '_img_o1 = NULL;\n'
    blockTemplate.functionCall = '\n	if(block' + blockTemplate.blockNumber + '_img_i1)\n	{\n' + \
                                 '		double scale;\n	int H;\n	int W;\n' + \
                                 '		W = block' + blockTemplate.blockNumber + '_img_i1->width;\n' + \
                                 '		H = block' + blockTemplate.blockNumber + '_img_i1->height;\n' + \
                                 '		block' + blockTemplate.blockNumber + '_img_o1 = cvCreateImage(cvSize(W,H),block' + blockTemplate.blockNumber + '_img_i1->depth,block' + blockTemplate.blockNumber + '_img_i1->nChannels);\n' + \
                                 '		CvMat* mat = cvCreateMat(2,3,CV_32FC1);\n'
    if isCenter == "true":
        blockTemplate.functionCall += '		CvPoint2D32f center = cvPoint2D32f(W/2, H/2);\n'
    else:
        blockTemplate.functionCall += '		CvPoint2D32f center = cvPoint2D32f(' + str(int(float(xC))) + ',' + str(
            int(float(yC))) + ');\n'

    if isScalling == "true":
        blockTemplate.functionCall += '		scale = H/(fabs(H*sin(rads(90-abs(block' + blockTemplate.blockNumber + '_double_i2)))) + fabs(W*sin(rads(abs(block' + blockTemplate.blockNumber + '_double_i2)))));\n' + \
                                      '		cv2DRotationMatrix(center,block' + blockTemplate.blockNumber + '_double_i2,scale,mat);\n'
    else:
        blockTemplate.functionCall += '		cv2DRotationMatrix(center,block' + blockTemplate.blockNumber + '_double_i2,1.0,mat);\n'

    if isFilling == "true":
        blockTemplate.functionCall += '		cvWarpAffine(block' + blockTemplate.blockNumber + '_img_i1,block' + blockTemplate.blockNumber + '_img_o1,mat,CV_WARP_FILL_OUTLIERS,cvScalarAll(0));\n'
    else:
        blockTemplate.functionCall += '		cvWarpAffine(block' + blockTemplate.blockNumber + '_img_i1,block' + blockTemplate.blockNumber + '_img_o1,mat,0,cvScalarAll(0));\n'

    blockTemplate.functionCall += '	}\n'
    blockTemplate.dealloc = 'cvReleaseImage(&block' + blockTemplate.blockNumber + '_img_o1);\n' + \
                            'cvReleaseImage(&block' + blockTemplate.blockNumber + '_img_i1);\n'


# ------------------------------------------------------------------------------
# Block Setup
# ------------------------------------------------------------------------------
def getBlock():
    return {"Label": _("Rotate Image"),
            "Path": {"Python": "rotate",
                     "Glade": "glade/rotate.ui",
                     "Xml": "xml/rotate.xml"},
            "Inputs": 2,
            "Outputs": 1,
            "Icon": "images/rotate.png",
            "Color": "90:5:10:150",
            "InTypes": {0: "HRP_IMAGE", 1: "HRP_DOUBLE"},
            "OutTypes": {0: "HRP_IMAGE"},
            "Description": _("Rotates input image the input angle degrees. (More options inside)"),
            "TreeGroup": _("Experimental")
            }
