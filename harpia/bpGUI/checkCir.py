# -*- coding: utf-8 -*-
# [HARPIA PROJECT]
#[Ourobolos Project UFSJ]
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

        filename = self.m_sDataDir + 'glade/checkCir.ui'
        self.m_oPropertiesXML = PropertiesXML
        self.m_oS2iBlockProperties = S2iBlockProperties

        widget_list = [
            'Properties',
            'dpSel',
            'distSel',
            'threshSel',
            'qualySel',
            'minX',
            'maxX',
            'minY',
            'maxY',
            'minRad',
            'maxRad',
            'numOfCircs',
            'PosCirc',
            'NumCirc',
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

            name = Property.getAttr("name")
            value = Property.getAttr("value")

            if name == "dpSel":
                self.widgets['dpSel'].set_value(float(value));
            if name == "distSel":
                self.widgets['distSel'].set_value(float(value));
            if name == "threshSel":
                self.widgets['threshSel'].set_value(float(value));
            if name == "qualySel":
                self.widgets['qualySel'].set_value(float(value));
            if name == "minX":
                self.widgets['minX'].set_value(float(value));
            if name == "maxX":
                self.widgets['maxX'].set_value(float(value));
            if name == "minY":
                self.widgets['minY'].set_value(float(value));
            if name == "maxY":
                self.widgets['maxY'].set_value(float(value));
            if name == "minRad":
                self.widgets['minRad'].set_value(float(value));
            if name == "maxRad":
                self.widgets['maxRad'].set_value(float(value));
            if name == "numOfCircs":
                self.widgets['numOfCircs'].set_value(float(value));
            if name == "criteria":
                if value == "pos":
                    self.widgets['PosCirc'].set_active(True);
                elif value == "num":
                    self.widgets['NumCirc'].set_active(True);

        self.configure()

    # ----------------------------------------------------------------------

    def __del__(self):
        pass

    # ----------------------------------------------------------------------

    def on_prop_confirm_clicked(self, *args):
        self.widgets['prop_confirm'].grab_focus()

        for Property in self.block_properties:

            name = Property.getAttr("name")

            if name == "dpSel":
                Property.setAttr("value", unicode(self.widgets['dpSel'].get_value()))
            if name == "distSel":
                Property.setAttr("value", unicode(self.widgets['distSel'].get_value()))
            if name == "threshSel":
                Property.setAttr("value", unicode(self.widgets['threshSel'].get_value()))
            if name == "qualySel":
                Property.setAttr("value", unicode(self.widgets['qualySel'].get_value()))
            if name == "minX":
                Property.setAttr("value", unicode(self.widgets['minX'].get_value()))
            if name == "maxX":
                Property.setAttr("value", unicode(self.widgets['maxX'].get_value()))
            if name == "minY":
                Property.setAttr("value", unicode(self.widgets['minY'].get_value()))
            if name == "maxY":
                Property.setAttr("value", unicode(self.widgets['maxY'].get_value()))
            if name == "minRad":
                Property.setAttr("value", unicode(self.widgets['minRad'].get_value()))
            if name == "maxRad":
                Property.setAttr("value", unicode(self.widgets['maxRad'].get_value()))
            if name == "numOfCircs":
                Property.setAttr("value", unicode(self.widgets['numOfCircs'].get_value()))
            if name == "criteria":
                if self.widgets['NumCirc'].get_active():
                    Property.setAttr("value", u"num")
                elif self.widgets['PosCirc'].get_active():
                    Property.setAttr("value", u"pos")

        self.m_oS2iBlockProperties.SetPropertiesXML(self.m_oPropertiesXML)

        self.m_oS2iBlockProperties.SetBorderColor(self.m_oBorderColor)
        self.m_oS2iBlockProperties.SetBackColor(self.m_oBackColor)
        self.widgets['Properties'].destroy()

    # ----------------------------------------------------------------------
    def getHelp(self):
        return 'Aplica a transformada de Hough para a deteccao de circulos.\nDetecta formas circulares na imagem de entrada. Saida 1 é a resposta da avaliacao(*) e a saida dois mostra os circulos encontrados.'

##propProperties = Properties()()
# propProperties.show( center=0 )

# ------------------------------------------------------------------------------
# Code generation
# ------------------------------------------------------------------------------
def generate(blockTemplate):
    for propIter in blockTemplate.properties:
        if propIter[0] == 'dpSel':
            dpSel = propIter[1]
        elif propIter[0] == 'distSel':
            distSel = propIter[1]
        elif propIter[0] == 'threshSel':
            threshSel = propIter[1]
        elif propIter[0] == 'qualySel':
            qualySel = propIter[1]
        elif propIter[0] == 'minX':
            minX = propIter[1]
        elif propIter[0] == 'maxX':
            maxX = propIter[1]
        elif propIter[0] == 'minY':
            minY = propIter[1]
        elif propIter[0] == 'maxY':
            maxY = propIter[1]
        elif propIter[0] == 'minRad':
            minRad = propIter[1]
        elif propIter[0] == 'maxRad':
            maxRad = propIter[1]
        elif propIter[0] == 'numOfCircs':
            numOfCircs = propIter[1]
        elif propIter[0] == 'criteria':
            checkCrit = propIter[1]

    if checkCrit == 'pos':
        circType = 0
    elif checkCrit == 'num':
        circType = 1

    blockTemplate.imagesIO = \
        'IplImage * block' + blockTemplate.blockNumber + '_img_i1 = NULL;\n' + \
        'IplImage * block' + blockTemplate.blockNumber + '_img_t1 = NULL;\n' + \
        'CvSeq * block' + blockTemplate.blockNumber + '_circs = NULL;\n' + \
        'float * PCircs' + blockTemplate.blockNumber + ' = NULL;\n' + \
        'CvMemStorage * block' + blockTemplate.blockNumber + '_storage = NULL;\n' + \
        'int block' + blockTemplate.blockNumber + '_it;\n' + \
        'IplImage * block' + blockTemplate.blockNumber + '_img_o2 = NULL;\n' + \
        'double block' + blockTemplate.blockNumber + '_double_o1;\n'
    blockTemplate.functionCall = '\nif(block' + blockTemplate.blockNumber + '_img_i1){\n' + \
                                 '	block' + blockTemplate.blockNumber + '_storage = cvCreateMemStorage(0);\n' + \
                                 '	block' + blockTemplate.blockNumber + '_img_t1 = cvCreateImage(cvGetSize(block' + blockTemplate.blockNumber + '_img_i1),8,1);\n' + \
                                 '	if(block' + blockTemplate.blockNumber + '_img_i1->nChannels != 1)\n' + \
                                 '		cvCvtColor(block' + blockTemplate.blockNumber + '_img_i1, block' + blockTemplate.blockNumber + '_img_t1, CV_BGR2GRAY);\n' + \
                                 '	else\n' + \
                                 '		cvCopyImage(block' + blockTemplate.blockNumber + '_img_i1, block' + blockTemplate.blockNumber + '_img_t1);\n' + \
                                 '	cvSmooth(block' + blockTemplate.blockNumber + '_img_t1, block' + blockTemplate.blockNumber + '_img_t1, CV_GAUSSIAN, 9, 9, 0,0 );\n' + \
                                 '	block' + blockTemplate.blockNumber + '_circs = cvHoughCircles( block' + blockTemplate.blockNumber + '_img_t1, block' + blockTemplate.blockNumber + '_storage, CV_HOUGH_GRADIENT, ' + dpSel + ', ' + distSel + ', ' + threshSel + ', ' + qualySel + ',0,1000);\n' + \
                                 '	block' + blockTemplate.blockNumber + '_double_o1 = 0;\n'
    if circType == 0:
        blockTemplate.functionCall += '	for(block' + blockTemplate.blockNumber + '_it = 0; block' + blockTemplate.blockNumber + '_it < block' + blockTemplate.blockNumber + '_circs->total;block' + blockTemplate.blockNumber + '_it++){\n' + \
                                      '		PCircs' + blockTemplate.blockNumber + ' = (float*)cvGetSeqElem( block' + blockTemplate.blockNumber + '_circs, block' + blockTemplate.blockNumber + '_it );\n' + \
                                      '		if(cvRound(PCircs' + blockTemplate.blockNumber + '[2]) > ' + minRad + ' && cvRound(PCircs' + blockTemplate.blockNumber + '[2]) < ' + maxRad + ')\n' + \
                                      '			if( cvRound(PCircs' + blockTemplate.blockNumber + '[0]) > ' + minX + ' && cvRound(PCircs' + blockTemplate.blockNumber + '[0]) < ' + maxX + ')\n' + \
                                      '				if(cvRound(PCircs' + blockTemplate.blockNumber + '[1]) > ' + minY + ' && cvRound(PCircs' + blockTemplate.blockNumber + '[1]) < ' + maxY + ')\n' + \
                                      '					block' + blockTemplate.blockNumber + '_double_o1 = 1.0;\n' + \
                                      '	}\n'
    else:
        blockTemplate.functionCall += '	if(block' + blockTemplate.blockNumber + '_circs->total >= ' + str(
            int(float(numOfCircs))) + ')\n' + \
                                      '		block' + blockTemplate.blockNumber + '_double_o1 = 1.0;\n'

    blockTemplate.functionCall += '	block' + blockTemplate.blockNumber + '_img_o2 = cvCloneImage(block' + blockTemplate.blockNumber + '_img_i1);\n' + \
                                  '	for(block' + blockTemplate.blockNumber + '_it = 0; block' + blockTemplate.blockNumber + '_it < block' + blockTemplate.blockNumber + '_circs->total;block' + blockTemplate.blockNumber + '_it++){\n' + \
                                  '		PCircs' + blockTemplate.blockNumber + ' = (float*)cvGetSeqElem( block' + blockTemplate.blockNumber + '_circs, block' + blockTemplate.blockNumber + '_it );\n' + \
                                  '		cvCircle( block' + blockTemplate.blockNumber + '_img_o2, cvPoint(cvRound(PCircs' + blockTemplate.blockNumber + '[0]),cvRound(PCircs' + blockTemplate.blockNumber + '[1])), cvRound(PCircs' + blockTemplate.blockNumber + '[2]), CV_RGB(255,0,0), 3, 8, 0 );\n' + \
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
    return {"Label": _("Detect Hough Circles"),
            "Path": {"Python": "checkCir",
                     "Glade": "glade/checkCir.ui",
                     "Xml": "xml/checkCir.xml"},
            "Icon": "images/checkCir.png",
            "Color": "20:20:60:150",
            "InTypes": {0: "HRP_IMAGE"},
            "OutTypes": {0: "HRP_DOUBLE", 1: "HRP_IMAGE"},
            "Description": _(
                "Output1: Returns 1 if the desired circle was found, 0 otherwise.\n Output2: The input image with the detected circles red-tagged"),
            "TreeGroup": _("Feature Detection")
            }
