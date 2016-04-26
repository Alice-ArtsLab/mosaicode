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
        # t_oS2iHelp = XMLParser(self.m_sDataDir + 'help/findSquares' + _('_en.help'))

        # t_oTextBuffer = gtk.TextBuffer()

        # t_oTextBuffer.set_text(unicode(str(t_oS2iHelp.getTag("help").getTag("content").getTagContent())))

        # self.widgets['HelpView'].set_buffer(t_oTextBuffer)

    # ----------------------------------------------------------------------

    def __del__(self):
        pass
 
    # ----------------------------------------------------------------------

    def getHelp(self):
        return "Detecta formas circulares na imagem de entrada.\
        Saida 1 é a resposta da avaliacao(*)\
        e a saida dois mostra os circulos encontrados."

    #----------------------------------------------------------------------

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
    blockTemplate.header += r"""

//Routines to findSquares
double angle( CvPoint* pt1, CvPoint* pt2, CvPoint* pt0 )
{
		double dx1 = pt1->x - pt0->x;
		double dy1 = pt1->y - pt0->y;
		double dx2 = pt2->x - pt0->x;
		double dy2 = pt2->y - pt0->y;
		return (dx1*dx2 + dy1*dy2)/sqrt((dx1*dx1 + dy1*dy1)*(dx2*dx2 + dy2*dy2) + 1e-10);
}

CvSeq* findSquares4( IplImage* img, CvMemStorage* storage, int minArea, int maxArea)
{
		CvSeq* contours;
		int i, c, l, N = 11;
		int thresh = 50;
		CvSize sz = cvSize( img->width & -2, img->height & -2 );
		IplImage* timg = cvCloneImage( img ); // make a copy of input image
		IplImage* gray = cvCreateImage( sz, 8, 1 ); 
		IplImage* pyr = cvCreateImage( cvSize(sz.width/2, sz.height/2), 8, 3 );
		IplImage* tgray;
		CvSeq* result;
		double s, t;

		if(minArea == -1)
			minArea = 0;
		if(maxArea == -1)
			maxArea = (img->width * img->height);

		CvSeq* squares = cvCreateSeq( 0, sizeof(CvSeq), sizeof(CvPoint), storage );
		

		cvSetImageROI( timg, cvRect( 0, 0, sz.width, sz.height ));
		
		// down-scale and upscale the image to filter out the noise
		cvPyrDown( timg, pyr, CV_GAUSSIAN_5x5 );
		cvPyrUp( pyr, timg, CV_GAUSSIAN_5x5 );
		tgray = cvCreateImage( sz, 8, 1 );
		
		// find squares in every color plane of the image
		for( c = 0; c < 3; c++ ){
				// extract the c-th color plane
				cvSetImageCOI( timg, c+1 );
				cvCopy( timg, tgray, 0 );
				for( l = 0; l < N; l++ )
				{
						if( l == 0 )
						{
								cvCanny( tgray, gray, 0, thresh, 5 );
								cvDilate( gray, gray, 0, 1 );
						}
						else
						{
								cvThreshold( tgray, gray, (l+1)*255/N, 255, CV_THRESH_BINARY );
						}
						cvFindContours( gray, storage, &contours, sizeof(CvContour),
								CV_RETR_LIST, CV_CHAIN_APPROX_SIMPLE, cvPoint(0,0) );
						while( contours )
						{
								result = cvApproxPoly( contours, sizeof(CvContour), storage,
										CV_POLY_APPROX_DP, cvContourPerimeter(contours)*0.02, 0 );
								if( result->total == 4 &&
										fabs(cvContourArea(result,CV_WHOLE_SEQ)) > minArea &&
										fabs(cvContourArea(result,CV_WHOLE_SEQ)) < maxArea &&
										cvCheckContourConvexity(result) )
								{
										s = 0;
										
										for( i = 0; i < 5; i++ )
										{
												if( i >= 2 )
												{
														t = fabs(angle(
														(CvPoint*)cvGetSeqElem( result, i ),
														(CvPoint*)cvGetSeqElem( result, i-2 ),
														(CvPoint*)cvGetSeqElem( result, i-1 )));
														s = s > t ? s : t;
												}
										}
										if( s < 0.3 )
												for( i = 0; i < 4; i++ )
														cvSeqPush( squares,
																(CvPoint*)cvGetSeqElem( result, i ));
								}
								contours = contours->h_next;
						}
				}
		}
		cvReleaseImage( &gray );
		cvReleaseImage( &pyr );
		cvReleaseImage( &tgray );
		cvReleaseImage( &timg );
		return squares;
}

double drawSquares( IplImage* cpy, CvSeq* squares )
{
		CvSeqReader reader;
		int i;
		cvStartReadSeq( squares, &reader, 0 );
		for( i = 0; i < squares->total; i += 4 )
		{
				CvPoint pt[4], *rect = pt;
				int count = 4;
				CV_READ_SEQ_ELEM( pt[0], reader );
				CV_READ_SEQ_ELEM( pt[1], reader );
				CV_READ_SEQ_ELEM( pt[2], reader );
				CV_READ_SEQ_ELEM( pt[3], reader );
				cvPolyLine( cpy, &rect, &count, 1, 1, CV_RGB(0,255,0), 3, CV_AA, 0 );
		}
	return (double)squares->total;
}

//End of routines to findSquares

			"""

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
        'IplImage * block$$_img_i1 = NULL;\n' + \
        'IplImage * block$$_img_o2 = NULL;\n' + \
        'double block$$_double_o1;\n' + \
        'CvMemStorage * block$$_storage = NULL;\n'

    blockTemplate.functionCall = '\nif(block$$_img_i1){\n' + \
                                 '	block$$_img_o2 = cvCloneImage(block$$_img_i1);\n' + \
                                 '	block$$_storage = cvCreateMemStorage(0);\n' + \
                                 '	block$$_double_o1 = (double)drawSquares( block$$_img_o2, findSquares4( block$$_img_o2, block$$_storage , ' + str(minVal) + ', ' + str(maxVal) + ') );\n' + \
                                 '	cvClearMemStorage( block$$_storage );\n' + \
                                 '}\n'

    blockTemplate.dealloc = 'cvReleaseImage(&block$$_img_o2);\n' + \
                            'cvReleaseImage(&block$$_img_i1);\n' + \
                            'cvReleaseMemStorage(&block$$_storage );\n'


# ------------------------------------------------------------------------------
# Block Setup
# ------------------------------------------------------------------------------
def getBlock():
    return {'Label': _('Find Squares'),
            'Path': {'Python': 'findSquares',
                     'Glade': 'glade/findSquares.ui',
                     'Xml': 'xml/findSquares.xml'},
            'Icon': 'images/findSquares.png',
            'Color': '50:50:200:150',
            'InTypes': {0: 'HRP_IMAGE'},
            'OutTypes': {0: "HRP_DOUBLE", 1: "HRP_IMAGE"},
            'Description': _(
                'Finds four-sided polygons on the input image.\n Output 1 = Number of detected Polygons\n Output 2 = The input image tagged with the found polygons.'),
            'TreeGroup': _('Feature Detection')
            }
