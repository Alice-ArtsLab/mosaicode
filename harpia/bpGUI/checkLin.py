# -*- coding: utf-8 -*-
# [HARPIA PROJECT]
# [Ourobolos Project UFSJ]
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

        filename = self.m_sDataDir + 'glade/checkLin.ui'
        self.m_oPropertiesXML = PropertiesXML
        self.m_oS2iBlockProperties = S2iBlockProperties

        widget_list = [
            'Properties',
            'qThresh',
            'minC',
            'maxG',
            'aX',
            'aY',
            'aR',
            'bX',
            'bY',
            'bR',
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
            name = Property.getAttr("name")
            value = Property.getAttr("value")

            if name == "qThresh":
                self.widgets['qThresh'].set_value(float(value));
            if name == "minC":
                self.widgets['minC'].set_value(float(value));
            if name == "maxG":
                self.widgets['maxG'].set_value(float(value));
            if name == "aX":
                self.widgets['aX'].set_value(float(value));
            if name == "aY":
                self.widgets['aY'].set_value(float(value));
            if name == "aR":
                self.widgets['aR'].set_value(float(value));
            if name == "bX":
                self.widgets['bX'].set_value(float(value));
            if name == "bY":
                self.widgets['bY'].set_value(float(value));
            if name == "bR":
                self.widgets['bR'].set_value(float(value));

        self.configure()

        # # load help text
        # t_oS2iHelp = XMLParser(self.m_sDataDir + "help/checkLin" + _("_en.help"))

        # t_oTextBuffer = gtk.TextBuffer()

        # t_oTextBuffer.set_text(unicode(str(t_oS2iHelp.getTag("help").getTag("content").getTagContent())))

        # self.widgets['HelpView'].set_buffer(t_oTextBuffer)

    # ----------------------------------------------------------------------

    def __del__(self):
        pass

    # ----------------------------------------------------------------------

    def on_prop_confirm_clicked(self, *args):
        self.widgets['prop_confirm'].grab_focus()

        for Property in self.block_properties:
            name = Property.getAttr("name")
            
            if name == "qThresh":
                 Property.setAttr("value", unicode(self.widgets['qThresh'].get_value()))
            if name == "minC":
                Property.setAttr("value", unicode(self.widgets['minC'].get_value()))
            if name == "maxG":
                Property.setAttr("value", unicode(self.widgets['maxG'].get_value()))
            if name == "aX":
                Property.setAttr("value", unicode(self.widgets['aX'].get_value()))
            if name == "aY":
                Property.setAttr("value", unicode(self.widgets['aY'].get_value()))
            if name == "aR":
                Property.setAttr("value", unicode(self.widgets['aR'].get_value()))
            if name == "bX":
                Property.setAttr("value", unicode(self.widgets['bX'].get_value()))
            if name == "bY":
                Property.setAttr("value", unicode(self.widgets['bY'].get_value()))
            if name == "bR":
                Property.setAttr("value", unicode(self.widgets['bR'].get_value()))

        self.m_oS2iBlockProperties.SetPropertiesXML(self.m_oPropertiesXML)

        self.m_oS2iBlockProperties.SetBorderColor(self.m_oBorderColor)
        self.m_oS2iBlockProperties.SetBackColor(self.m_oBackColor)
        self.widgets['Properties'].destroy()

        # ----------------------------------------------------------------------
    def getHelp(self):
        return 'Aplica a transformada de Hough para a deteccao de linhas.\nDetecta formas que se assemelhem a linhas na imagem de entrada. Saida 1 é a resposta da avaliacao(*) e a saida dois mostra as linhas encontradas.'


# propProperties = Properties()()
# propProperties.show( center=0 )

# ------------------------------------------------------------------------------
# Code generation
# ------------------------------------------------------------------------------
def generate(blockTemplate):
    for propIter in blockTemplate.properties:
        if propIter[0] == 'qThresh':
            qThresh = propIter[1]
        elif propIter[0] == 'minC':
            minC = propIter[1]
        elif propIter[0] == 'maxG':
            maxG = propIter[1]
        elif propIter[0] == 'aX':
            aX = propIter[1]
        elif propIter[0] == 'aY':
            aY = propIter[1]
        elif propIter[0] == 'aR':
            aR = propIter[1]
        elif propIter[0] == 'bX':
            bX = propIter[1]
        elif propIter[0] == 'bY':
            bY = propIter[1]
        elif propIter[0] == 'bR':
            bR = propIter[1]
        elif propIter[0] == 'disDraw':
            disDraw = propIter[1]

    blockTemplate.imagesIO = \
        'IplImage * block' + blockTemplate.blockNumber + '_img_i1 = NULL;\n' + \
        'IplImage * block' + blockTemplate.blockNumber + '_img_t1 = NULL;\n' + \
        'CvSeq * block' + blockTemplate.blockNumber + '_lines = NULL;\n' + \
        'CvMemStorage * block' + blockTemplate.blockNumber + '_storage = NULL;\n' + \
        'int block' + blockTemplate.blockNumber + '_it;\n' + \
        'IplImage * block' + blockTemplate.blockNumber + '_img_o2 = NULL;\n' + \
        'double block' + blockTemplate.blockNumber + '_double_o1;\n' + \
        'int b' + blockTemplate.blockNumber + 'dX,b' + blockTemplate.blockNumber + 'dY;\n'
    blockTemplate.functionCall = '\nif(block' + blockTemplate.blockNumber + '_img_i1){\n' + \
                                 '	block' + blockTemplate.blockNumber + '_storage = cvCreateMemStorage(0);\n' + \
                                 '	block' + blockTemplate.blockNumber + '_img_t1 = cvCreateImage(cvGetSize(block' + blockTemplate.blockNumber + '_img_i1),8,1);\n' + \
                                 '	if(block' + blockTemplate.blockNumber + '_img_i1->nChannels != 1)\n' + \
                                 '		cvCvtColor(block' + blockTemplate.blockNumber + '_img_i1, block' + blockTemplate.blockNumber + '_img_t1, CV_BGR2GRAY);\n' + \
                                 '	else\n' + \
                                 '		cvCopyImage(block' + blockTemplate.blockNumber + '_img_i1, block' + blockTemplate.blockNumber + '_img_t1);\n' + \
                                 '	cvCanny(block' + blockTemplate.blockNumber + '_img_t1, block' + blockTemplate.blockNumber + '_img_t1, 50, 200, 3);\n' + \
                                 '	block' + blockTemplate.blockNumber + '_lines = cvHoughLines2( block' + blockTemplate.blockNumber + '_img_t1, block' + blockTemplate.blockNumber + '_storage, CV_HOUGH_PROBABILISTIC, 1, CV_PI/180, ' + qThresh + ', ' + minC + ', ' + maxG + ' );\n' + \
                                 '	block' + blockTemplate.blockNumber + '_double_o1 = 0;\n' + \
                                 '	for(block' + blockTemplate.blockNumber + '_it = 0; block' + blockTemplate.blockNumber + '_it < block' + blockTemplate.blockNumber + '_lines->total;block' + blockTemplate.blockNumber + '_it++)\n' + \
                                 '	{\n' + \
                                 '		CvPoint* line = (CvPoint*)cvGetSeqElem( block' + blockTemplate.blockNumber + '_lines, block' + blockTemplate.blockNumber + '_it );\n' + \
                                 '		b' + blockTemplate.blockNumber + 'dX = line[0].x - ' + aX + ';\n' + \
                                 '		b' + blockTemplate.blockNumber + 'dY = line[0].y - ' + aY + ';\n' + \
                                 '		if((int)cvSqrt((float)(b' + blockTemplate.blockNumber + 'dX*b' + blockTemplate.blockNumber + 'dX + b' + blockTemplate.blockNumber + 'dY*b' + blockTemplate.blockNumber + 'dY)) <= ' + aR + ')\n' + \
                                 '		{\n' + \
                                 '			b' + blockTemplate.blockNumber + 'dX = line[1].x - ' + bX + ';\n' + \
                                 '			b' + blockTemplate.blockNumber + 'dY = line[1].y - ' + bY + ';\n' + \
                                 '			if((int)cvSqrt((float)(b' + blockTemplate.blockNumber + 'dX*b' + blockTemplate.blockNumber + 'dX + b' + blockTemplate.blockNumber + 'dY*b' + blockTemplate.blockNumber + 'dY)) <= ' + bR + ')\n' + \
                                 '				block' + blockTemplate.blockNumber + '_double_o1 = 1.0;\n' + \
                                 '		}\n' + \
                                 '	}\n'
    if disDraw == "no":
        blockTemplate.functionCall += '	block' + blockTemplate.blockNumber + '_img_o2 = cvCloneImage(block' + blockTemplate.blockNumber + '_img_i1);\n' + \
                                      '	for(block' + blockTemplate.blockNumber + '_it = 0; block' + blockTemplate.blockNumber + '_it < block' + blockTemplate.blockNumber + '_lines->total;block' + blockTemplate.blockNumber + '_it++)\n	{\n' + \
                                      '		CvPoint* line = (CvPoint*)cvGetSeqElem( block' + blockTemplate.blockNumber + '_lines, block' + blockTemplate.blockNumber + '_it );\n' + \
                                      '		cvLine( block' + blockTemplate.blockNumber + '_img_o2, line[0], line[1], CV_RGB(255,0,0), 2, 8, 0);\n' + \
                                      '	}\n'

    blockTemplate.functionCall += '}\n'

    blockTemplate.dealloc = 'cvReleaseImage(&block' + blockTemplate.blockNumber + '_img_o2);\n' + \
                            'cvReleaseImage(&block' + blockTemplate.blockNumber + '_img_t1);\n' + \
                            'cvReleaseMemStorage(&block' + blockTemplate.blockNumber + '_storage);\n' + \
                            'cvReleaseImage(&block' + blockTemplate.blockNumber + '_img_i1);\n'


# ------------------------------------------------------------------------------
# Block Setup
# ------------------------------------------------------------------------------
def getBlock():
    return {"Label": _("Detect Hough Lines"),
            "Path": {"Python": "checkLin",
                     "Glade": "glade/checkLin.ui",
                     "Xml": "xml/checkLin.xml"},
            "Icon": "images/checkLin.png",
            "Color": "80:20:130:150",
            "InTypes": {0: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_DOUBLE", 1: "HRP_IMAGE"},
            "Description": _(
                "Output1: Returns 1 if the desired line was found, 0 otherwise.\n Output2: The input image with the detected lines red-tagged"),
            "TreeGroup": _("Feature Detection")
            }
