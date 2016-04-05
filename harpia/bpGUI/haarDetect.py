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
from harpia.filefilters import * 

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

        filename = self.m_sDataDir + 'glade/haarDetect.ui'
        self.m_oPropertiesXML = PropertiesXML
        self.m_oS2iBlockProperties = S2iBlockProperties

        widget_list = [
            'Properties',
            'ACQULabelFilename',
            'ACQUFilename',
            'min_neighbors',
            'ACQUButtonSearch',
            'BackgroundColor',
            'BorderColor',
            'HelpView',
            'acquisition_confirm'
        ]

        handlers = [
            'on_ACQUButtonSearch_clicked',
            'on_BackColorButton_clicked',
            'on_BorderColorButton_clicked',
            'on_acquisition_confirm_clicked',
            'on_cancel_clicked'
        ]

        top_window = 'Properties'

        GladeWindow.__init__(self, filename, top_window, widget_list, handlers)

        self.m_sCurrentActive = 'file'
        # load properties values

        self.block_properties = self.m_oPropertiesXML.getTag("properties").getTag("block").getChildTags("property")

        for Property in self.block_properties:

            name = Property.getAttr("name")
            value = Property.getAttr("value")
            if name == "cascade_name":
                self.widgets['ACQUFilename'].set_text(value);
            if name == "min_neighbors":
                self.widgets['min_neighbors'].set_value(int(float(value)));

        # load block state
        t_bState = self.m_oS2iBlockProperties.GetState()

        self.configure()

        # load help text
        # t_oS2iHelp = XMLParser("../etc/acquisition/acquisition.help")
        # t_oS2iHelp = XMLParser(self.m_sDataDir + "help/haarDetect" + _("_en.help"))

        # t_oTextBuffer = gtk.TextBuffer()

        # t_oTextBuffer.set_text(unicode(str(t_oS2iHelp.getTag("help").getTag("content").getTagContent())))

        # self.widgets['HelpView'].set_buffer(t_oTextBuffer)

    # ----------------------------------------------------------------------

    def __del__(self):
        pass

    # ----------------------------------------------------------------------

    def on_acquisition_confirm_clicked(self, *args):
        self.widgets['acquisition_confirm'].grab_focus()
        t_sFilename = unicode(self.widgets['ACQUFilename'].get_text())

        for Property in self.block_properties:
            name = Property.getAttr("name")
            # file selected
            if name == "cascade_name":
                Property.setAttr("value", unicode(t_sFilename))
            if name == 'min_neighbors':
                Property.setAttr("value", unicode(self.widgets['min_neighbors'].get_value()))

        self.m_oS2iBlockProperties.SetPropertiesXML(self.m_oPropertiesXML)

        self.m_oS2iBlockProperties.SetBorderColor(self.m_oBorderColor)

        self.m_oS2iBlockProperties.SetBackColor(self.m_oBackColor)

        self.widgets['Properties'].destroy()

    # ----------------------------------------------------------------------
    def getHelp(self):
        return "Detecta formas circulares na imagem de entrada. Saida 1 é a resposta da avaliacao(*) e a saida dois mostra os circulos encontrados."



    #----------------------------------------------------------------------

    def on_ACQUButtonSearch_clicked(self, *args):

        dialog = gtk.FileChooserDialog("Abrir...",
                                       None,
                                       gtk.FILE_CHOOSER_ACTION_OPEN,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_OPEN, gtk.RESPONSE_OK))

        dialog.set_default_response(gtk.RESPONSE_OK)

        # -------------
        # Scotti
        if os.name == 'posix':
            dialog.set_current_folder("/home/" + str(os.getenv('USER')) + "/Desktop")
        # Scotti

        dialog.add_filter(AllFileFilter())
        dialog.add_filter(XMLImageFileFilter())

        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            response = dialog.get_filename()
        elif response == gtk.RESPONSE_CANCEL:
            response = None
        dialog.destroy()

        self.widgets['ACQUFilename'].set_text(response);

    # ----------------------------------------------------------------------

    def on_ACQURadioFile_pressed(self, *args):
        self.widgets['ACQULabelFilename'].set_sensitive(True)
        self.widgets['ACQUFilename'].set_sensitive(True)
        self.widgets['ACQUButtonSearch'].set_sensitive(True)

        # ----------------------------------------------------------------------


# AcquisitionProperties = Properties( )
# AcquisitionProperties.show( center=0 )

# ------------------------------------------------------------------------------
# Code generation
# ------------------------------------------------------------------------------
def generate(blockTemplate):
    for propIter in blockTemplate.properties:
        if propIter[0] == 'cascade_name':
            cascade_name = os.path.expanduser(propIter[1])
        elif propIter[0] == 'min_neighbors':
            t_sMinNeighbors = propIter[1]
    blockTemplate.imagesIO = \
        'IplImage * block$$_img_i1 = NULL;\n' + \
        'CvPoint block$$_point_o1 = cvPoint(0,0);\n' + \
        'CvRect block$$_rect_o2 = cvRect( 0, 0, 1, 1);\n' + \
        'IplImage * block$$_img_o3 = NULL;\n' + \
        'double block$$_double_o4 = 0.0;\n' + \
        'static CvMemStorage* block$$_storage = 0;\n' + \
        'static CvHaarClassifierCascade* block$$_cascade = 0;\n' + \
        'const char* block$$_cascade_name = "' + cascade_name + '";\n'
    blockTemplate.functionCall = '\nif(block$$_img_i1){\n' + \
                                 '	double scale = 1.3;\n' + \
                                 '	block$$_cascade = (CvHaarClassifierCascade*)cvLoad( block$$_cascade_name, 0, 0, 0 );\n' + \
                                 '	IplImage* gray = cvCreateImage( cvSize(block$$_img_i1->width,block$$_img_i1->height), 8, 1 );\n' + \
                                 '	IplImage* small_img = cvCreateImage( cvSize( cvRound (block$$_img_i1->width/scale), cvRound (block$$_img_i1->height/scale)),8, 1 );\n' + \
                                 '	cvCvtColor( block$$_img_i1, gray, CV_BGR2GRAY );\n' + \
                                 '	cvResize( gray, small_img, CV_INTER_LINEAR );\n' + \
                                 '	cvEqualizeHist( small_img, small_img );\n' + \
                                 '	if(!block$$_img_o3)\n' + \
                                 '	block$$_img_o3 = cvCloneImage(block$$_img_i1);\n' + \
                                 '	cvCopy(block$$_img_i1,block$$_img_o3,0);\n' + \
                                 '	block$$_storage = cvCreateMemStorage(0);\n' + \
                                 '	cvClearMemStorage( block$$_storage );\n' + \
                                 '	block$$_rect_o2 = cvRect( 0, 0, 1, 1);\n' + \
                                 '	CvSeq* faces = cvHaarDetectObjects( small_img, block$$_cascade, block$$_storage,1.1, ' + t_sMinNeighbors + ', 0/*CV_HAAR_DO_CANNY_PRUNING*/,cvSize(30, 30) );\n' + \
                                 '	block$$_double_o4 = faces->total;\n' + \
                                 '	if(faces)\n' + \
                                 '	{\n' + \
                                 '		int i;\n' + \
                                 '		for( i = 0; i < (faces ? faces->total : 0); i++ )\n' + \
                                 '		{\n' + \
                                 '		CvRect* r = (CvRect*)cvGetSeqElem( faces, i );\n' + \
                                 '			if(r)\n' + \
                                 '			{\n' + \
                                 '				CvPoint center;\n' + \
                                 '				int radius;\n' + \
                                 '				center.x = cvRound((r->x + r->width*0.5)*scale);\n' + \
                                 '				center.y = cvRound((r->y + r->height*0.5)*scale);\n' + \
                                 '				radius = cvRound((r->width + r->height)*0.25*scale);\n' + \
                                 '				cvCircle( block$$_img_o3, center, radius, cvScalarAll(0), 3, 8, 0 );\n' + \
                                 '				if(i == 0)\n' + \
                                 '				{\n' + \
                                 '					block$$_point_o1 = center;\n' + \
                                 '					block$$_rect_o2.x = (r->x)*scale;\n' + \
                                 '					block$$_rect_o2.y = (r->y)*scale;\n' + \
                                 '					block$$_rect_o2.width = (r->width)*scale;\n' + \
                                 '					block$$_rect_o2.height = (r->height)*scale;\n' + \
                                 '				}\n' + \
                                 '			}\n' + \
                                 '		}\n' + \
                                 '	}\n' + \
                                 '	cvReleaseImage( &gray );\n' + \
                                 '	cvReleaseImage( &small_img );\n' + \
                                 '}\n'
    blockTemplate.dealloc = 'cvReleaseImage(&block$$_img_o3);\n' + \
                            'cvReleaseImage(&block$$_img_i1);\n' + \
                            'cvReleaseMemStorage(&block$$_storage);\n'


# ------------------------------------------------------------------------------
# Block Setup
# ------------------------------------------------------------------------------
def getBlock():
    return {'Label': _('Haar (face) Detector'),
            'Path': {'Python': 'haarDetect',
                     'Glade': 'glade/haarDetect.ui',
                     'Xml': 'xml/haarDetect.xml'},
            'Icon': 'images/haarDetect.png',
            'Color': '50:220:40:150',
            'InTypes': {0: 'HRP_IMAGE'},
            'OutTypes': {0: 'HRP_POINT', 1: 'HRP_RECT', 2: 'HRP_IMAGE', 3: 'HRP_DOUBLE'},
            'Description': _('Haar (face) Detector finds regions on the input image according to the given haar-classifier. \n First Output is the center of the first \
detected feature, second is a rectangle around the first detected feature and the third is the input image with the detected features tagged by a red circle.\n \
The last output is the number of detected faces.'),
            'TreeGroup': _("Feature Detection")
            }
